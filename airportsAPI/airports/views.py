from rest_framework import generics, viewsets
from .serializers import AirlineSerializer, AirplaneSerializer, CountrySerializer, AirportSerializer
from .serializers import DetailedAirplaneSerializer, DetailedAirportSerializer
from .models import Airline, Airplane, Country, Airport


class AirplaneListCreateAV(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    
class AirplaneRetriveUpdateDestroyAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = DetailedAirplaneSerializer
    lookup_url_kwarg = 'id'


class AirlineViewSet(viewsets.ModelViewSet):
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    
    
class AirportListCreateAV(generics.ListCreateAPIView):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()

class AirportRetriveUpdateDestroyAV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailedAirportSerializer
    queryset = Airport.objects.all()
    lookup_url_kwarg = 'id'