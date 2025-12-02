from rest_framework import serializers
from .models import CustomUser


class DetailedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', "first_name", "last_name", "email", "username", "phone_number"]