from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from .serializers import FlightSerializer, TicketSerializer, OrderSerializer, DetailedOrderSerializer
from .models import Flight, Ticket, Order
from users.models import CustomUser


# i see some flights with rows/columns available.
# i create order to buy 1 or more available tickets(i guees there is no need to check if ticket available, cuz system will show already what can i choose and what I can't)
# so in order the amount is creating, created_at and pending status(waiting to buy a ticket(but what about cash? Should I remove it?))
# Well, I waited the payment, and updated_at is updated..
# so that's creation of order. (ticket_status -> booked)

# should I manage ability to edit it?(after payment no), but i need be able to refund it and payback
# so here i need to set ticket_status from avail to cancelled 

# okay, let's talk about overall logic. Countries, airports, airline is created and stay still for a long.
# flights, orders, tickets is changing very often, user also.
# so airline creates flights, where flights creates tickets. Users using orders to buy a ticket

# should i make groups: airline stuff, default users, just superusers/staff?

class OrderListCreate(ListCreateAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def create(self, validated_data):
        # serializer = OrderSerializer(data=self.request.data, read_only=True)  

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
    # queryset = Order.objects.all()
    serializer_class = DetailedOrderSerializer
    lookup_url_kwarg = 'id'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    
        
# class FlightViewSet(viewsets.ModelViewSet):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer

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
    
    

        
    #     return Ticket.objects.filter(user=self.request.user)
    # def create(self, request):
    #     serializer = TicketSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True) 

    #     row = serializer.validated_data['row']
    #     column = serializer.validated_data['column']

    #     try:
    #         ticket = Ticket.objects.get(row=row, column=column)
    #     except:
    #         ticket = None
            
    #     if ticket:    
    #         if ticket.ticket_status in ["used", "booked"]:
    #             return Response(f"The seat is {ticket.ticket_status}", status=status.HTTP_400_BAD_REQUEST)
        
    #     flight = serializer.validated_data['flight'] 
    #     plane = flight.plane
    #     max_row = plane.max_row
    #     max_column = plane.max_column
        
    #     if row <= max_row and column <= max_column:
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     return Response("No available seats", status=status.HTTP_400_BAD_REQUEST) # not sure what method to use
                   