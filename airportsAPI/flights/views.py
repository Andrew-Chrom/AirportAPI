from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from django.utils.timezone import now
from .serializers import FlightSerializer, TicketSerializer, OrderSerializer, CreateOrderSerializer, PaymentSerializer
from .models import Flight, Ticket, Order, Payment
from users.models import CustomUser
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework.permissions import AllowAny
from .pagination import UserFlightPagination, AdminFlightPagination
from rest_framework.pagination import PageNumberPagination, CursorPagination
import time

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

HOST = 'https://saleable-calceolate-carolyne.ngrok-free.dev'
SUCCESS_URL = f'{HOST}/success'
CANCEL_URL = f'{HOST}/cancelled'

@api_view(['GET'])
def Success(request):
    return Response({'succesfully paid'})

@api_view(['GET'])
def Cancelled(request):
    return Response({'Cancelled'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except ValueError:
        return Response({'detail': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return Response({'detail': 'Invalid signature'}, status=400)

    if event['type'] ==  'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        
        if order_id:
            payment = Payment.objects.create(amount=session['amount_total'] / 100,
                                         status='completed',
                                         order_id=order_id)
            payment.save()
            
            Order.objects.filter(id=order_id).update(
                status='completed',
                updated_at=now()
            )
            Ticket.objects.filter(order=order_id).update(ticket_status='booked')

    elif event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)

                if order.status == 'pending':
                    order.status = 'cancelled'

                    order.save()
                    Ticket.objects.filter(order=order).update(
                        ticket_status='available', 
                        order=None 
                    )
            except Order.DoesNotExist:
                return Response("Order doesn't exist", status=404)
    
    return Response({'status': 'success'}, status=200)

class OrderListCreate(ListCreateAPIView):
    
    def get_queryset(self):
        qs = Order.objects.select_related("user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = CustomUser.objects.get(id=data["user"])
        ticket_ids = data["tickets"]
        
        with transaction.atomic():
            tickets = Ticket.objects.filter(id__in=ticket_ids)
            if tickets.count() != len(ticket_ids):
                return Response({"error": "Some tickets do not exist"}, status=400)

            for t in tickets:
                if t.ticket_status != "available":
                    return Response({"error": f"Ticket {t.id} is not available"}, status=400)

            total_amount = sum(t.price for t in tickets)

            order = Order.objects.create(
                user=user,
                amount=total_amount,
                status="pending"
            )

            for t in tickets:
                t.order = order
                t.ticket_status = 'reserved'
                t.save()

            expiration_time = int(time.time()) + (30 * 60)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'Order #{order.id}'},
                        'unit_amount': int(order.amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=SUCCESS_URL,
                cancel_url=CANCEL_URL,
                metadata={'order_id': order.id},
                expires_at=expiration_time
            )

            return Response({"checkout_url": session.url}, status=201) 
        return Response(status=status.HTTP_400_BAD_REQUEST)
class OrderRetrieveUpdateDestroy(RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'id'
    
    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("tickets")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

class FlightUserApiView(ListAPIView):
    pagination_class = UserFlightPagination
    serializer_class = FlightSerializer
    queryset = Flight.objects.select_related("plane", "departure_airport", "arrival_airport")

class FlightAdminApiView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = AdminFlightPagination
    serializer_class = FlightSerializer
    queryset = Flight.objects.select_related("plane", "departure_airport", "arrival_airport")
    
 
class FlightUpdateApiView(APIView):
    permission_classes = [IsAdminUser]
    
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
        
    def delete(self, request, id):
        try:
            flight = Flight.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        flight.delete()
        return Response(status=status.HTTP_200_OK)

        
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('user', 'order', 'flight')
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['flight', 'ticket_status', 'ticket_type']
   
   
class AvailableTicketsView(ListAPIView):
    serializer_class = TicketSerializer 
    def get_queryset(self):
        flight_id = self.kwargs['id']
        return Ticket.objects.select_related('user', 'order', 'flight').filter(flight__id=flight_id, ticket_status='available')
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('order')
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['order', 'status']