from rest_framework import serializers
from .models import Airline, Airplane


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'airline_name', 'airline_alias', 'contact_info']

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'airplane_name', 'manufacturer', 'max_row', 'max_column', 'commisioning_year', 'airline']