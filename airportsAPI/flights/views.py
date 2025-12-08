from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from .serializers import FlightSerializer, TicketSerializer, OrderSerializer, DetailedOrderSerializer
from .models import Flight, Ticket, Order
from users.models import CustomUser

class OrderListCreate(ListCreateAPIView):
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return DetailedOrderSerializer
        return OrderSerializer

    def create(self, validated_data): 

        tickets_data = validated_data.data.pop('tickets')
        user_id = validated_data.data.pop('user')
        
        order = Order.objects.create(**validated_data.data, user=CustomUser.objects.get(id=user_id))
       
        amount = 0
        for ticket in tickets_data:
            t = Ticket.objects.get(id=ticket)
            print(t.ticket_status, "$"*50)
            if t.ticket_status != "available":
                return Response("All tickets is not available", status=status.HTTP_404_NOT_FOUND)
            t.order = order
            t.ticket_status = "booked"
            t.save()
            amount += t.price
        order.amount = amount
        order.save()
        
        serializer = OrderSerializer(data=order).data
        if serializer.is_valid():
            return Response(serializer.data)        
        else:
            return Response(serializer.errors)
class OrderRetrieveUpdateDestroy(RetrieveDestroyAPIView):
    serializer_class = DetailedOrderSerializer
    lookup_url_kwarg = 'id'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

class FlightApiView(APIView):
    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
 
class FlightUpdateApiView(APIView):
    def get(self, request, id):
        try:
            flight = Flight.objects.get(pk=id)
        except:
            return Response("flight doesn't exist with pk={pk}")
        
        serializer = FlightSerializer(flight)
        return Response(serializer.data)
            
    def put(self, request, id):
        try:
            flight = Flight.objects.get(pk=id)
        except:
            return Response("flight doesn't exist with pk={pk}")
        
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['flight']
   
   
class AvailableTicketsView(ListAPIView):
    serializer_class = TicketSerializer 
    def get_queryset(self):
        flight_id = self.kwargs['id']
        return Ticket.objects.filter(flight__id=flight_id, ticket_status='available')