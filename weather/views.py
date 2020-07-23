from django.shortcuts import render
from .forms import CityForm, FilterForm
from .models import  Weather
from django.views import View
from django.views.generic import ListView, FormView
from django.core.paginator import Paginator


import datetime
import requests
import pytz

class IndexView(View):
    form_class = CityForm
    template_name = "weather/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather = self.get_current_weather(city)
            if 'city' in weather.keys():
                weather_to_db = self.get_weather(city)
                self.save_to_db(weather_to_db, city)
            context = {'form': form, 'weather': weather}

            return render(request, self.template_name, context=context)
        return render(request, self.template_name, {'form': form})



    def get_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=214eb92b337eee6a6b689da021294f39"
        weather_data = []
        city_weather = requests.get(url.format(city)).json()

        try:
            for keys in city_weather['list']:
                weather = {
                    'city': city,
                    'temperature': keys['main']['temp'],
                    'humidity': keys['main']['humidity'],
                    'icon': keys['weather'][0]['icon'],
                    'description': keys['weather'][0]['description'],
                    'wind_speed': keys['wind']['speed'],
                    'wind_direction': keys['wind']['deg'],
                    'date': datetime.datetime(2013, 11, 20, 20, 8, 7, 127325,tzinfo=pytz.UTC).strptime(keys['dt_txt'], "%Y-%m-%d %H:%M:%S"),
                }
                weather_data.append(weather)
        except KeyError:
            return False
        return weather_data

    def get_current_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=214eb92b337eee6a6b689da021294f39"
        city_weather = requests.get(url.format(city)).json()

        if (city_weather['cod'] == '404'):
            message = "City not found. Lets try again."
            return {'message': message}
        else:
            weather = {
                    'city': city,
                    'temperature': city_weather['main']['temp'],
                    'humidity': city_weather['main']['humidity'],
                    'icon': city_weather['weather'][0]['icon'],
                    'description': city_weather['weather'][0]['description'],
                    'wind_speed': city_weather['wind']['speed'],
                    'wind_direction': city_weather['wind']['deg'],
                    'time': datetime.datetime.fromtimestamp(int(city_weather['dt'])).strftime('%Y-%m-%d %H:%M:%S'),
            }
            return weather

    def save_to_db(self, array, city):
        counter = Weather.objects.filter(city=city).count()
        if counter == 0:
            list_of_object = []
            for item in array:
                list_of_object.append(Weather(**item))
            Weather.objects.bulk_create(list_of_object)


class WeatherList(ListView, FormView):
    template_name = "weather/cities.html"
    queryset = Weather.objects.all()
    form_class = FilterForm
    paginator_class = Paginator
    paginate_by = 3


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather = Weather.objects.filter(city=city)
            context = {'form': form, 'weather': weather}
            print(context)
            return render(request, self.template_name, context=context)
        return render(request, self.template_name, {'form': form})
