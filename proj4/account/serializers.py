from rest_framework import serializers
from .models import Account, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
