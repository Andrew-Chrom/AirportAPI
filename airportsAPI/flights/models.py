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
    
    flight_status = models.CharField(
        max_length=10,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )
    
    plane = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.departure_airport.id} - {self.arrival_airport.id} | {self.departure_time} - {self.arrival_time}" # | {self.departure_airport.name} - {self.arrival_airport.name}" # need to change

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        BOOKED    = "booked", "BOOKED"
        CANCELLED = "cancelled", "CANCELLED"
        USED      = "used", "USED"
        AVAILABLE = "available", "AVAILABLE"
    class TicketType(models.TextChoices):
        ECONOMY  = "economy", "ECONOMY"
        PREMIUM  = "premium", "PREMIUM"
        BUSINESS = "business", "BUSINESS"
        FIRST    = "first", "FIRST"
    
    price = models.FloatField()
    
    row = models.IntegerField(null=True)
    column = models.CharField(max_length=1, null=True) # A, B, C
    
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