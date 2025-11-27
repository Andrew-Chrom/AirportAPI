from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import FlightSerializer, TicketSerializer
from .models import Flight, Ticket


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['flight']
    
    
    def create(self, request):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 

        row = serializer.validated_data['row']
        column = serializer.validated_data['column']

        try:
            ticket = Ticket.objects.get(row=row, column=column)
        except:
            ticket = None
            
        if ticket:    
            if ticket.ticket_status in ["used", "booked"]:
                return Response(f"The seat is {ticket.ticket_status}", status=status.HTTP_400_BAD_REQUEST)
        
        flight = serializer.validated_data['flight'] 
        plane = flight.plane
        max_row = plane.max_row
        max_column = plane.max_column
        
        if row <= max_row and column <= max_column:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response("No available seats", status=status.HTTP_400_BAD_REQUEST) # not sure what method to use
                   