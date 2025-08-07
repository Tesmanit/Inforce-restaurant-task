from rest_framework import serializers
from django.contrib.auth.models import User

from restaurant.models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'calories', 'price', 'image']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    day = serializers.DateField(required=False)
    class Meta:
        model = Menu
        fields = ['id', 'name', 'day', 'dishes']