from rest_framework import viewsets
from .serializers import CountrySerializer, AirportSerializer
from .models import Country, Airport

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
class AirportViewSet(viewsets.ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    