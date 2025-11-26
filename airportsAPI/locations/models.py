from django.db import models
from aviation.models import Airline

class Country(models.Model):
    class RegionType(models.TextChoices):
        EUROPE = "europe", "EU"
        ASIA   = "asia", "AS"
        AMERICA = "america", "AM"
        AFRICA  = "africe", "AF"
    
    country_name = models.CharField(max_length=100)
    region       = models.CharField(
        max_length=10,
        choices=RegionType.choices,
        default=None
    )

    def __str__(self):
        return self.country_name

class Airport(models.Model):
    name      = models.CharField(max_length=100, default=None)
    latitude  = models.FloatField()
    longitude = models.FloatField()
    
    runaway_num = models.PositiveIntegerField() # к-сть злітних смуг
    plane_num   = models.PositiveIntegerField() # num of planes in airport
    
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    airlines = models.ManyToManyField(Airline, blank=True) # Airport can have many airlines and airline can be placed in many airports
    
    def __str__(self):
        return self.name