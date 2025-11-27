from rest_framework.routers import SimpleRouter
from .views import AirlineViewSet, AirplaneViewSet

router = SimpleRouter()
router.register(r'airlines', AirlineViewSet, basename='airline')
router.register(r'airplanes', AirplaneViewSet, basename='airplane')

urlpatterns = router.urls