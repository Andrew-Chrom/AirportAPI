from rest_framework.routers import SimpleRouter
from .views import CountryViewSet, AirportViewSet

router = SimpleRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'airports', AirportViewSet, basename='airport')

urlpatterns = router.urls
