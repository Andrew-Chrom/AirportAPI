from rest_framework.routers import SimpleRouter
from .views import AirlineViewSet, AirplaneListCreateApiView, AirplaneRetriveUpdateDestroyApiView, CountryViewSet, AirportListCreateApiView, AirportRetriveUpdateDestroyApiView
from rest_framework.urls import path

router = SimpleRouter()

router.register(r'countries', CountryViewSet, basename='country')
router.register(r'airlines', AirlineViewSet, basename='airline')

urlpatterns = [
    path('airports/', AirportListCreateApiView.as_view()),
    path('airports/<int:id>/', AirportRetriveUpdateDestroyApiView.as_view()),

    path('airplanes/', AirplaneListCreateApiView.as_view()),
    path('airplanes/<int:id>/', AirplaneRetriveUpdateDestroyApiView.as_view())
]

urlpatterns += router.urls
