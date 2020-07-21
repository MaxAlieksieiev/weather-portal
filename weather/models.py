from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"

class Weather(models.Model):
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    date = models.TimeField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()
