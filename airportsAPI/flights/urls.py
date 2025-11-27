from rest_framework.routers import SimpleRouter
from .views import FlightViewSet, TicketViewSet

router = SimpleRouter()
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = router.urls