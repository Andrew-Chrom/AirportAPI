from rest_framework.routers import SimpleRouter
from .views import FlightViewSet, TicketViewSet, OrderViewSet

router = SimpleRouter()
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'orders', OrderViewSet, basename="order")

urlpatterns = router.urls