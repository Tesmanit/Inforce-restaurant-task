from django.db import models
from restaurant.models import Restaurant
from django.contrib.auth.models import User


class Employee(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
        verbose_name='Restaurant', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        verbose_name='User', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} employee of {self.restaurant.name}'