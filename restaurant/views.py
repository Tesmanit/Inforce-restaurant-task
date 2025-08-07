from datetime import date

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q

from restaurant.models import Menu, Dish, Restaurant, Vote
from employees.models import Employee
from restaurant.serializers import (
    MenuSerializer,
    RestaurantCreateSerializer,
    MenuVoteSerializerV1,
    MenuVoteSerializerV2,
    VoteCreateSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    http_method_names = ["post"]
    permission_classes = [permissions.IsAdminUser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        restaurant_name = request.data.get("restaurant_name")
        restaurant_user_password = request.data.get("restaurant_user_password")

        if not restaurant_name or not restaurant_user_password:
            return Response(
                "restaurant_name, restaurant_user_password are required fields",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=restaurant_name).exists():
            return Response(
                "User with this nickname already exists",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=restaurant_name, password=restaurant_user_password
        )
        user.save()
        restaurant = Restaurant.objects.create(name=restaurant_name, user=user)
        serializer = RestaurantCreateSerializer(restaurant)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class MenuViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get"]
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.filter(day=date.today()).prefetch_related("dishes")

    def get_queryset(self):
        # filtering queryset for fetching user be either owner or employee of particular restaurant
        queryset = (
            super()
            .get_queryset()
            .filter(
                Q(restaurant__employee__user=self.request.user)
                | Q(restaurant__user=self.request.user)
            )
        )

        if not queryset.exists():
            raise PermissionDenied("You do not have permission to view these objects.")

        return queryset

    def perform_create(self, serializer):
        # checking if user is restaurant
        try:
            restaurant = self.request.user.restaurant_model
        except Restaurant.DoesNotExist:
            raise ValidationError("You are not a restaurant representative.")

        dish_ids = self.request.data.get("dish_ids", [])
        if not dish_ids:
            raise ValidationError("dish_ids are required.")
        dishes = Dish.objects.filter(id__in=dish_ids)
        if dishes.count() != len(dish_ids):
            raise ValidationError("One or more dish IDs are invalid.")
        if self.request.data.get("day"):
            day = self.request.data.get("day")
        else:
            day = date.today()
        menus = Menu.objects.filter(
            day=day, restaurant=self.request.user.restaurant_model
        )
        for menu in menus:
            menu_dish_ids = set(menu.dishes.values_list("id", flat=True))
            new_dish_ids = set(dish_ids)
            if menu_dish_ids == new_dish_ids:
                raise ValidationError("You already have the same menu for that day")

        menu = serializer.save(restaurant=restaurant, day=day)
        menu.dishes.set(dishes)


class VotesViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get"]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        menus = (
            Menu.objects.filter(day=date.today())
            .filter(
                Q(restaurant__employee__user=request.user)
                | Q(restaurant__user=request.user)
            )
            .annotate(vote_count=Count("votes"))
        )
        if request.app_version.startswith("1"):
            serializer = MenuVoteSerializerV1(menus, many=True)
        if request.app_version.startswith("2"):
            serializer = MenuVoteSerializerV2(menus, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {}
        data["menu_id"] = request.data.get("menu_id")
        employee = Employee.objects.get(user=request.user)
        data["employee_id"] = employee.id
        serializer = VoteCreateSerializer(data=data)
        if serializer.is_valid():
            vote = Vote(**serializer.validated_data)

            try:
                vote.clean()
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

            vote.save()
            return Response(
                "Vote has been succesfully added", status=status.HTTP_201_CREATED
            )
        return Response("Some data was invalid", status=status.HTTP_400_BAD_REQUEST)
