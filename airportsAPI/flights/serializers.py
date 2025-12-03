from rest_framework import serializers
from .models import Flight, Ticket, Order
from users.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'price', 'row', 'column', 'ticket_status', 'ticket_type', 'flight', 'user', 'order']

class DetailedOrderSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['amount', 'created_at', 'updated_at', 'payment_method', 'status', 'user', 'tickets']

class OrderSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'amount', 'created_at', 'status', 'user', 'tickets'] 
    
    
class CreateOrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'tickets'] 
        
    
    
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', 'flight_status', 'plane']
    

