from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Restaurant(models.Model):
    name = models.CharField(verbose_name='Restaurant name', max_length=30, blank=False)
    menu_of_the_day = models.OneToOneField('Menu', related_name='featured_in_restaurant', 
        on_delete=models.DO_NOTHING, verbose_name='Menu of the day', blank=True)
    user = models.OneToOneField(User, related_name='restaurant_model',
        on_delete=models.PROTECT, verbose_name='Representing user', blank=True)

    def __str__(self):
        return f'{self.name} restaurant'


class Menu(models.Model):
    name = models.CharField(verbose_name='Menu name', max_length=20, blank=False)
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE,
        verbose_name='Restaurant', blank=False)
    day = models.DateField(verbose_name='Day', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Menu {self.name} of {self.restaurant.name} restaurant'

# Non-unique dishes for testing purposes
class Dish(models.Model):
    name = models.CharField(verbose_name='Dish name', max_length=30, blank=False)
    calories = models.IntegerField(verbose_name='Amount of calories per unit')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # blank=True set for image for testing purposes
    image = models.ImageField(verbose_name='Dish image', blank=True)

    def __str__(self):
        return f'Dish {self.name}'


class Vote(models.Model):
    employee = models.ForeignKey('employees.Employee', related_name='votes',
        blank=False, verbose_name='Employee', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='votes',
        blank=False, verbose_name='Menu', on_delete=models.CASCADE)
    
    # pre-save function that restricts voting twice a day for 1 employee
    def clean(self):
        if Vote.objects.filter(employee=self.employee, menu__day=self.menu.day).exclude(pk=self.pk).exists():
            raise ValidationError('You have already voted for this day.')
        
    def __str__(self):
        return f'{self.employee} voted for {self.menu.name} menu'