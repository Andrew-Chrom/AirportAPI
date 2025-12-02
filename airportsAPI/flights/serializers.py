from rest_framework import serializers
from .models import Flight, Ticket, Order
from users.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'price', 'row', 'column', 'ticket_status', 'ticket_type', 'flight', 'user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    # amount = serializers.FloatField()
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()
    
    # status = serializers.ChoiceField(choices=("pending", "completed", "cancelled", "refunded"))
    # payment_method = serializers.ChoiceField(choices=("credit_card", "cash"))
    # user = UserSerializer() 
    # tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        
    
    
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', 'flight_status', 'plane']
    

