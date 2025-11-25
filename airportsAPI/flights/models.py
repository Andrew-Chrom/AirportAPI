from django.db import models
from django.db.models.functions import Now

from locations.models import Airports
from aviation.models import Airplanes
from users.models import CustomUser

class Flights(models.Model):
    class FlightStatus(models.TextChoices):
        SCHEDULED = "scheduled", "SCHEDULED"
        BOARDING  = "boarding", "BOARDING"
        DEPARTED  = "departed", "DEPARTED"
        DELAYED   = "delayed", "DELAYED"
        CANCELLED = "cancelled", "CANCELLED"
    
    departure_time = models.DateTimeField(db_default=Now())
    arrival_time   = models.DateTimeField(db_default=Now())

    departure_airport = models.ForeignKey(Airports, on_delete=models.DO_NOTHING) 
    arrival_airport   = models.ForeignKey(Airports, on_delete=models.DO_NOTHING)
    
    passenger_num = models.PositiveIntegerField() # num of sitting place
    flight_status = models.CharField(
        max_length=10,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )
    
    plane = models.ForeignKey(Airplanes, on_delete=models.DO_NOTHING)
    

class Tickets(models.Model):
    class TicketStatus(models.TextChoices):
        BOOKED    = "booked", "BOOKED"
        CANCELLED = "cancelled", "CANCELLED"
        USED      = "used", "USED"
    
    class TicketType(models.TextChoices):
        ECONOMY  = "economy", "ECONOMY"
        PREMIUM  = "premium", "PREMIUM"
        BUSINESS = "business", "BUSINESS"
        FIRST    = "first", "FIRST"
    
    price = models.FloatField()
    place = models.PositiveIntegerField()
    
    ticket_status = models.CharField(
        max_length=10,
        choices=TicketStatus.choices,
        default=TicketStatus.BOOKED
    )
    
    ticket_type = models.CharField(
        max_length=10,
        choices=TicketType.choices,
        default=TicketType.FIRST
    )
    
    flight = models.ForeignKey(Flights, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)