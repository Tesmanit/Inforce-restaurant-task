from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from restaurant.models import Menu, Restaurant, Dish
from employees.models import Employee
from datetime import date


class FullFlowTests(APITestCase):
    def setUp(self):
        self.employee_user = User.objects.create_user(
            username="employee", password="testpass"
        )
        self.restaurant = Restaurant.objects.create(
            name="MyPlace", user=self.employee_user
        )
        self.employee = Employee.objects.create(
            user=self.employee_user, restaurant=self.restaurant
        )

        self.dish = Dish.objects.create(name="Burger", calories=300, price=14.99)
        self.menu = Menu.objects.create(
            name="Lunch", restaurant=self.restaurant, day=date.today()
        )
        self.menu.dishes.add(self.dish)

        self.resto_user = User.objects.create_user(username="resto", password="pass123")
        self.resto = Restaurant.objects.create(name="Resto", user=self.resto_user)

    def test_employee_vote_success(self):
        self.client.force_authenticate(user=self.employee_user)
        url = reverse("votes-list")
        data = {"menu_id": self.menu.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, "Vote has been succesfully added")

    def test_employee_vote_twice_same_day(self):
        self.client.force_authenticate(user=self.employee_user)
        url = reverse("votes-list")
        data = {"menu_id": self.menu.id}
        self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("You have already voted for this day", str(response.data))

    def test_create_menu_invalid_dish_ids(self):
        self.client.force_authenticate(user=self.resto_user)
        url = reverse("menu-list")
        data = {"name": "Dinner", "dish_ids": [999, 888], "day": str(date.today())}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("One or more dish IDs are invalid", str(response.data))

    def test_create_menu_duplicate_same_day(self):
        self.client.force_authenticate(user=self.employee_user)
        url = reverse("menu-list")
        data = {"name": "Lunch", "dish_ids": [self.dish.id], "day": str(date.today())}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("You already have the same menu for that day", str(response.data))
