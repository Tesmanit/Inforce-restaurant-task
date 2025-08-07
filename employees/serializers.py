from rest_framework import serializers
from .models import Employee

class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'restaurant_id')
