from django.db import models
from django.db.models.functions import Now

class Airline(models.Model):
    airline_name = models.CharField(max_length=255)
    airline_alias = models.CharField(max_length=255)
    
    contact_info = models.CharField(max_length=100)
    
    def __str__(self):
        return self.airline_alias
    
class Airplane(models.Model):
    airplane_name = models.CharField(max_length=255)
    manufacturer  = models.CharField(max_length=255)
    
    max_row    = models.PositiveIntegerField(null=True)
    max_column = models.CharField(max_length=1, null=True) # A, B, C ..
     
    commisioning_year = models.PositiveIntegerField(null=True)
    airline = models.ForeignKey(Airline, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.airplane_name # not enough info?