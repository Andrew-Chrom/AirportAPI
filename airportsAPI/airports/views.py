from rest_framework import generics, viewsets, filters
from .serializers import AirlineSerializer, AirplaneSerializer, CountrySerializer, AirportSerializer
from .models import Airline, Airplane, Country, Airport
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

class AirplaneListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['airline', 'manufacturer']
    search_fields = ['name']
    
    queryset = Airplane.objects.select_related('airline')
    serializer_class = AirplaneSerializer
    
class AirplaneRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Airplane.objects.select_related('airline')
    serializer_class = AirplaneSerializer
    lookup_url_kwarg = 'id'

class AirlineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'alias']

class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region']
class AirportListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AirportSerializer
    queryset = Airport.objects.select_related('country').prefetch_related('airlines')

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['name', 'city']
class AirportRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AirportSerializer
    queryset = Airport.objects.select_related('country').prefetch_related('airlines')
    lookup_url_kwarg = 'id'