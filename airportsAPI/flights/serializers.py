from rest_framework import serializers
from .models import Flight, Ticket, Order, Payment

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'price', 'row', 'column', 'ticket_status', 'ticket_type', 'flight', 'user', 'order']

class OrderSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'amount', 'status', 'payment_method', 'created_at', 'updated_at', 'tickets']
        
class CreateOrderSerializer(serializers.Serializer):
    tickets = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    # user = serializers.IntegerField() 
    
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', 'flight_status', 'plane']
        
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'order', 'payment_date'] 