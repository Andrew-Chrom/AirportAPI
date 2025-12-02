from rest_framework.routers import SimpleRouter
from .views import TicketViewSet, OrderListCreate, OrderRetrieveUpdateDestroy, FlightApiView, FlightUpdateApiView
from django.urls import path


router = SimpleRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')   


urlpatterns = [
    path('orders/', OrderListCreate.as_view()),
    path('orders/<int:id>', OrderRetrieveUpdateDestroy.as_view()),
    path('flights/', FlightApiView.as_view()),
    path('flights/<int:id>', FlightUpdateApiView.as_view())
]

urlpatterns += router.urls