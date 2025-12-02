from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    
    contact_info = models.CharField(max_length=100)
    
    def __str__(self):
        return self.alias
    
class Airplane(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
     
    max_row = models.PositiveIntegerField(null=True)
    max_column = models.CharField(max_length=1, null=True) # A, B, C ..
     
    commisioning_year = models.PositiveIntegerField(null=True)
    airline = models.ForeignKey(Airline, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name

class Country(models.Model):
    class RegionType(models.TextChoices):
        EUROPE = "europe", "EU"
        ASIA = "asia", "AS"
        AMERICA = "america", "AM"
        AFRICA = "africe", "AF"
    
    name = models.CharField(max_length=100)
    region = models.CharField(
        max_length=10,
        choices=RegionType.choices,
        default=None
    )

    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100, default=None)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    runaway_num = models.PositiveIntegerField()
    plane_num = models.PositiveIntegerField() # num of planes in airport
    
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    airlines = models.ManyToManyField(Airline, blank=True) # Airport can have many airlines and airline can be placed in many airports
    
    def __str__(self):
        return self.name
    


