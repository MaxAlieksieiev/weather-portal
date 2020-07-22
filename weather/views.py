from django.shortcuts import render
from .forms import CityForm
from .models import City
from django.views import View
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie


import datetime
import requests


class IndexView(View):
    form_class = CityForm
    template_name = "weather/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            city = form.cleaned_data['name']

            weather_to_db = self.get_weather(city)
            weather = self.get_current_weather(city)

            context = {'form': form, 'weather': weather}

        return render(request, self.template_name, context=context)

    def get_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=214eb92b337eee6a6b689da021294f39"
        weather_data = []
        city_weather = requests.get(url.format(city)).json()

        if (city_weather['cod'] == '404'):
            message = "City not found. Lets try again."
            return message
        else:
            for keys in city_weather['list']:
                weather = {
                    'city': city,
                    'temperature': keys['main']['temp'],
                    'humidity': keys['main']['humidity'],
                    'icon': keys['weather'][0]['icon'],
                    'description': keys['weather'][0]['description'],
                    'wind_speed': keys['wind']['speed'],
                    'wind_direction': keys['wind']['deg'],
                    'date': keys['dt_txt'],
                }
                weather_data.append(weather)
            return weather_data

    def get_current_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=214eb92b337eee6a6b689da021294f39"
        city_weather = requests.get(url.format(city)).json()

        if (city_weather['cod'] == '404'):
            message = "City not found. Lets try again."
            return message
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

class WeatherList(ListView):
    template_name = "weather/cities.html"

