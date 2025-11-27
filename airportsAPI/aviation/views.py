from rest_framework import viewsets
from .serializers import AirlineSerializer, AirplaneSerializer
from .models import Airline, Airplane

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
