from rest_framework.routers import SimpleRouter
from .views import (
    TicketViewSet, 
    OrderListCreate, OrderRetrieveUpdateDestroy, FlightViewSet,
    # FlightAdminApiView, FlightUserApiView, 
    # FlightUpdateApiView, 
    AvailableTicketsView, 
    PaymentViewSet, stripe_webhook)
from django.urls import path


router = SimpleRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')   
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'flights', FlightViewSet, basename='flight')

urlpatterns = [
    path('orders/', OrderListCreate.as_view()),
    path('orders/<int:id>', OrderRetrieveUpdateDestroy.as_view()),

    path('flights/<int:id>/tickets/available/', AvailableTicketsView.as_view()),
    path('webhook/stripe/', stripe_webhook),
]

urlpatterns += router.urls