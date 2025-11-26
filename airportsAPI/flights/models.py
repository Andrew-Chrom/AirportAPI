from django.db import models
from django.db.models.functions import Now

from locations.models import Airport
from aviation.models import Airplane
from users.models import CustomUser

class Flight(models.Model):
    class FlightStatus(models.TextChoices):
        SCHEDULED = "scheduled", "SCHEDULED"
        BOARDING  = "boarding", "BOARDING"
        DEPARTED  = "departed", "DEPARTED"
        DELAYED   = "delayed", "DELAYED"
        CANCELLED = "cancelled", "CANCELLED"
    
    departure_time = models.DateTimeField(db_default=Now())
    arrival_time   = models.DateTimeField(db_default=Now())

    departure_airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="departure_airport") 
    arrival_airport   = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="arrival_airport")
    
    passenger_num = models.PositiveIntegerField() # num of sitting place
    flight_status = models.CharField(
        max_length=10,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )
    
    plane = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return str(self.departure_time) # need to change

class Ticket(models.Model):
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
    
    # guess, that i need to change it on row and type(A, B, C ..)
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
    
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.flight.departure_airport.name} - {self.flight.departure_airport.name}" 