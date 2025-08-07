from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Employee, Restaurant
from .serializers import EmployeeCreateSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EmployeeCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        username = request.data.get('employee_username')
        password = request.data.get('employee_password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        restaurant_id = request.data.get('restaurant_id')

        if not username or not password or not restaurant_id:
            return Response( 'employee_username, employee_password, restaurant_id are required',
                status=status.HTTP_400_BAD_REQUEST)

        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        if User.objects.filter(username=username).exists():
            return Response('User with this nickname already exists', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        employee = Employee.objects.create(user=user, restaurant=restaurant)

        serializer = self.get_serializer(employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
