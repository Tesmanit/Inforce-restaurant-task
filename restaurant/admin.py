from django.contrib import admin
from .models import Menu, Restaurant, Dish, Vote

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Vote)
