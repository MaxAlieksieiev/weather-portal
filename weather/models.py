from django.db import models

# Create your models here.

class Weather(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    city = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    date = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = "weather"
        ordering = ['date']
