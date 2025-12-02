from rest_framework import viewsets
from .serializers import DetailedUserSerializer
from .models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = DetailedUserSerializer