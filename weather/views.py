from django.shortcuts import render
from .forms import CityForm
import datetime

import requests
# Create your views here.

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=214eb92b337eee6a6b689da021294f39"

    if request.method == "POST":
        city_form = CityForm(request.POST)

        if city_form.is_valid():
            city = city_form.cleaned_data['city']

            city_weather = requests.get(url.format(city)).json()

            if(city_weather['cod'] == '404'):
                message = "City not found. Lets try again."
                return render(request, 'weather/index.html', {'message': message, 'form': city_form})
            else:
                weather = {
                    'city': city,
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'humidity': city_weather['main']['humidity'],
                    'wind': city_weather['wind']['speed'],
                    'direction': city_weather['wind']['deg'],
                    'time': datetime.datetime.fromtimestamp(int(city_weather['dt'])).strftime('%Y-%m-%d %H:%M:%S'),
                    'icon': city_weather['weather'][0]['icon'],
                }
                context = {"weather": weather, "form": city_form}

                return render(request, 'weather/index.html', context=context)

    else:
        city_form = CityForm()

    return render(request, "weather/index.html", {'form': city_form})