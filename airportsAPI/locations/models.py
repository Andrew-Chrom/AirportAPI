from django.db import models
from aviation.models import Airlines

class Countries(models.Model):
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

class Airports(models.Model):
    latitude  = models.FloatField()
    longitude = models.FloatField()
    
    runaway_num = models.PositiveIntegerField() # к-сть злітних смуг
    plane_num   = models.PositiveIntegerField() # num of planes in airport
    
    country = models.ForeignKey(Countries, on_delete=models.DO_NOTHING)
    airlines = models.ManyToManyField(Airlines) # Airport can have many airlines and airline can be placed in many airports