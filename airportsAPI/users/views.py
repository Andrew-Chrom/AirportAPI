from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer
from .models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields    = ['username', 'first_name', 'last_name', 'email']