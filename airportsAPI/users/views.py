from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import DetailedUserSerializer
from .models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = DetailedUserSerializer
    permission_classes = [IsAdminUser]