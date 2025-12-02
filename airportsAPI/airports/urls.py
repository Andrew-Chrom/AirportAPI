from rest_framework.routers import SimpleRouter
from .views import AirlineViewSet, AirplaneListCreateAV, AirplaneRetriveUpdateDestroyAV, CountryViewSet, AirportListCreateAV, AirportRetriveUpdateDestroyAV
from rest_framework.urls import path

router = SimpleRouter()

# router.register(r'airplanes', AirplaneViewSet, basename='airplane')

router.register(r'countries', CountryViewSet, basename='country')
# router.register(r'airports', AirportViewSet, basename='airport')
router.register(r'airlines', AirlineViewSet, basename='airline')

urlpatterns = [
    path('airports/', AirportListCreateAV.as_view()),
    path('airports/<int:id>', AirportRetriveUpdateDestroyAV.as_view()),

    path('airplanes/', AirplaneListCreateAV.as_view()),
    path('airplanes/<int:id>/', AirplaneRetriveUpdateDestroyAV.as_view())
]

urlpatterns += router.urls
