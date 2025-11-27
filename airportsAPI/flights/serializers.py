from rest_framework import serializers
from .models import Flight, Ticket

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', 'flight_status', 'plane']
    

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'price', 'row', 'column', 'ticket_status', 'ticket_type', 'flight', 'user']