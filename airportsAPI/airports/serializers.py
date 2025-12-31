from rest_framework import serializers
from .models import Airline, Airplane, Country, Airport

import re

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'alias', 'contact_info']

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'name', 'manufacturer', 'max_row', 'max_column', 'commisioning_year', 'airline']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'region']

    def validate_country_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('name should be at least 3 characters in length')
        elif not re.match(r"^[A-Za-z\- ]+$", value):
            raise serializers.ValidationError('name should contain only A-Z and a-z characters')
        return value
    
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'latitude', 'longitude', 'city', 'runway_num', 'plane_num', 'country', 'airlines']
