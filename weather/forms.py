from django.forms import ModelForm, TextInput, Form, CharField, DateTimeField

from .models import Weather

class CityForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city']
        widgets = {
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }

class FilterForm(Form):
    city = CharField(max_length=255, required=False, widget=TextInput(attrs={'class': 'city-input'}))
    date_from = DateTimeField(required=False)
    date_to = DateTimeField(required=False)
