from django.db import models
from django.db.models.functions import Now

class Airlines(models.Model):
    airline_name = models.CharField(max_length=255)
    airline_alias = models.CharField(max_length=255)
    
    contact_info = models.CharField(max_length=100)
    
    
class Airplanes(models.Model):
    airplane_name = models.CharField(max_length=255)
    manufacturer  = models.CharField(max_length=255)
    
    seat_num = models.PositiveIntegerField()
    # Maybe just field with year will be enough, cuz there is no need to store exact date.
    commisioning_date = models.DateTimeField(db_default=Now()) # start date
    retirement_date = models.DateTimeField() 
    
    airline = models.ForeignKey(Airlines, on_delete=models.DO_NOTHING)
    