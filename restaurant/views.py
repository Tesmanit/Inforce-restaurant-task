from datetime import date

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from restaurant.models import Menu, Dish, Restaurant
from restaurant.serializers import MenuSerializer, RestaurantCreateSerializer


class MenuViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # checking if user is restaurant
        try:
            restaurant = self.request.user.restaurant_model
        except Restaurant.DoesNotExist:
            raise ValidationError('You are not a restaurant representative.')

        dish_ids = self.request.data.get('dish_ids', [])
        if not dish_ids:
            raise ValidationError('dish_ids are required.')
        dishes = Dish.objects.filter(id__in=dish_ids)
        if dishes.count() != len(dish_ids):
            raise ValidationError('One or more dish IDs are invalid.')
        if self.request.data.get('day'):
            day = self.request.data.get('day')
        else:
            day = date.today()
        menus = Menu.objects.filter(day=day, restaurant=self.request.user.restaurant_model)
        for menu in menus:
            menu_dish_ids = set(menu.dishes.values_list('id', flat=True))
            new_dish_ids = set(dish_ids)
            if menu_dish_ids == new_dish_ids:
                raise ValidationError('You already have the same menu for that day')
        
        menu = serializer.save(restaurant=restaurant, day=day)
        menu.dishes.set(dishes)