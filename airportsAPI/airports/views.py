from rest_framework import generics, viewsets
from .serializers import AirlineSerializer, AirplaneSerializer, CountrySerializer, AirportSerializer
from .serializers import DetailedAirplaneSerializer, DetailedAirportSerializer
from .models import Airline, Airplane, Country, Airport


class AirplaneListCreateApiView(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    
class AirplaneRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = DetailedAirplaneSerializer
    lookup_url_kwarg = 'id'


class AirlineViewSet(viewsets.ModelViewSet):
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    
    
class AirportListCreateApiView(generics.ListCreateAPIView):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()

class AirportRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailedAirportSerializer
    queryset = Airport.objects.all()
    lookup_url_kwarg = 'id'