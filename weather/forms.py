from django.forms import ModelForm, TextInput
from .models import Weather

class CityForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city']
        widgets = {
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }