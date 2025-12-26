from rest_framework import generics, viewsets
from .serializers import AirlineSerializer, AirplaneSerializer, CountrySerializer, AirportSerializer
from .serializers import DetailedAirplaneSerializer, DetailedAirportSerializer
from .models import Airline, Airplane, Country, Airport
from rest_framework.permissions import IsAdminUser

class AirplaneListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Airplane.objects.select_related('airline')
    serializer_class = AirplaneSerializer
    
class AirplaneRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Airplane.objects.select_related('airline')
    serializer_class = DetailedAirplaneSerializer
    lookup_url_kwarg = 'id'


class AirlineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    
    
class AirportListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AirportSerializer
    queryset = Airport.objects.select_related('country').prefetch_related('airlines')

class AirportRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DetailedAirportSerializer
    queryset = Airport.objects.select_related('country').prefetch_related('airlines')
    lookup_url_kwarg = 'id'