from rest_framework import serializers
from .models import Country, Airport

import re

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'region']

    def validate_country_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('country_name should be at least 3 characters in length')
        elif not re.match(r"^[A-Za-z\- ]$", value):
            raise serializers.ValidationError('country_name should contain only A-Z and a-z characters')
        return value
    
    
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'latitude', 'longitude', 'runaway_num', 'plane_num', 'country', 'airlines']
