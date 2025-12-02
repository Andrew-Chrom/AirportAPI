from django.db import models
from django.db.models.functions import Now
from airports.models import Airport, Airplane
from users.models import CustomUser

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "PENDING"
        COMPLETED = "completed", "COMPLETED"
        CANCELLED = "cancelled", "CANCELLED"
        REFUNDED = "refunded", "REFUNDED"
    
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = "credit_card", "CREDIT_CARD"
        CASH = "cash", "CASH"
    
    amount = models.FloatField(null=True)
    
    created_at = models.DateTimeField(db_default=Now())
    updated_at = models.DateTimeField(db_default=Now())
    
    
    payment_method = models.CharField(
        max_length=12,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CREDIT_CARD
    )
    
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Flight(models.Model):
    class FlightStatus(models.TextChoices):
        SCHEDULED = "scheduled", "SCHEDULED"
        BOARDING = "boarding", "BOARDING"
        DEPARTED = "departed", "DEPARTED"
        DELAYED = "delayed", "DELAYED"
        CANCELLED = "cancelled", "CANCELLED"
    
    departure_time = models.DateTimeField(db_default=Now())
    arrival_time = models.DateTimeField(db_default=Now())

    departure_airport = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="departure_airport") 
    arrival_airport   = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="arrival_airport")
    
    flight_status = models.CharField(
        max_length=10,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )
    
    plane = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)
    
    
    def save(self, **kwargs):
        is_new = self.pk is None
        
        super().save(**kwargs)
    
        if is_new:
            tickets = []
            columns = ['A', 'B', 'C', 'D', 'E', 'F']
            # investige if there are some logic when creating first, business, premium, economy class, then i need to add this 
            for row in range(1, self.plane.max_row + 1):
                for column in columns:
                    if column == self.plane.max_column:
                        tickets.append(Ticket(flight=self, row=row, column=column))
                        break
                    tickets.append(Ticket(flight=self, row=row, column=column))
            Ticket.objects.bulk_create(tickets)
    
    def __str__(self):
        return f"{self.departure_airport.id} - {self.arrival_airport.id} | {self.departure_time} - {self.arrival_time}" # | {self.departure_airport.name} - {self.arrival_airport.name}" # need to change

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        BOOKED = "booked", "BOOKED"
        CANCELLED = "cancelled", "CANCELLED"
        USED = "used", "USED"
        AVAILABLE = "available", "AVAILABLE"
    class TicketType(models.TextChoices):
        ECONOMY = "economy", "ECONOMY"
        PREMIUM = "premium", "PREMIUM"
        BUSINESS = "business", "BUSINESS"
        FIRST = "first", "FIRST"
    
    price = models.FloatField(null=True)
    
    row = models.IntegerField(null=True)
    column = models.CharField(max_length=1, null=True) # A, B, C
    
    ticket_status = models.CharField(
        max_length=10,
        choices=TicketStatus.choices,
        default=TicketStatus.AVAILABLE
    )
    
    ticket_type = models.CharField(
        max_length=10,
        choices=TicketType.choices,
        default=TicketType.FIRST
    )
    
    order = models.ForeignKey(Order, related_name="tickets", null=True, on_delete=models.DO_NOTHING)
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return f"{self.flight.departure_airport.name} - {self.flight.departure_airport.name}" 
    
    
