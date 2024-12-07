# yourapp/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['ID', 'Terms_Of_Use', 'Hashed_Password', 'Mother_Surname', 'Money_Left', 'User_Created']

