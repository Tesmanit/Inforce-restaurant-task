from rest_framework import serializers
from django.contrib.auth.models import User

from restaurant.models import Menu, Dish, Restaurant, Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RestaurantCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["name", "user"]


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "calories", "price", "image"]


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    day = serializers.DateField(required=False)

    class Meta:
        model = Menu
        fields = ["id", "name", "day", "dishes"]


class MenuVoteSerializerV1(serializers.ModelSerializer):
    vote_count = serializers.IntegerField()

    class Meta:
        model = Menu
        fields = ["id", "name", "vote_count"]


class MenuVoteSerializerV2(serializers.ModelSerializer):
    vote_count = serializers.IntegerField()

    class Meta:
        model = Menu
        fields = ["id", "name", "dishes", "vote_count"]


class VoteCreateSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(write_only=True)
    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vote
        fields = ["menu_id", "employee_id", "menu", "employee"]
        read_only_fields = ["menu", "employee"]
