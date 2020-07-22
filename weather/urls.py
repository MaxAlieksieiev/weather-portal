from django.urls import path
from .views import IndexView, WeatherList


urlpatterns = [
    path('', IndexView.as_view(), name="main"),
    path('show', WeatherList.as_view(), name="show"),
]