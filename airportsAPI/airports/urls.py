from rest_framework.routers import SimpleRouter
from .views import AirlineViewSet, AirplaneViewSet, CountryViewSet, AirportViewSet

router = SimpleRouter()
router.register(r'airlines', AirlineViewSet, basename='airline')
router.register(r'airplanes', AirplaneViewSet, basename='airplane')

router.register(r'countries', CountryViewSet, basename='country')
router.register(r'airports', AirportViewSet, basename='airport')

urlpatterns = router.urls
