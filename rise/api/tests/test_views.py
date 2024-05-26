from django.test import TestCase, Client
from django.urls import reverse
import json
from api.models import CustomUser, Expenses, ExpenseType, Suggestions, SuggestionType

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.expense_type = ExpenseType.objects.create(name="Food")
        self.suggestion_type = SuggestionType.objects.create(name="Save Energy")

    def test_register_user(self):
        # Удаляем пользователя, если он существует
        CustomUser.objects.filter(username=self.user_data['username']).delete()
        response = self.client.post(reverse('register_user'), json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json())

    def test_login_user(self):
        response = self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['user_id'], self.user.id)

    def test_get_user(self):
        self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        response = self.client.post(reverse('get_user'), json.dumps({"username": "testuser"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())

    def test_logout_user(self):
        self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        response = self.client.post(reverse('logout_user'), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # Перезагрузим сессии для обновления состояния
        self.client.logout()
        self.assertNotIn('user_id', self.client.session)

    def test_delete_user(self):
        self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        response = self.client.post(reverse('delete_user'), json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username="testuser").exists())

    def test_create_expenses(self):
        self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        expense_data = {
            "userID": self.user.id,
            "date": "25/05/2023",
            "amount": 100,
            "description": "Groceries",
            "typeID": self.expense_type.id
        }
        response = self.client.post(reverse('create_expenses'), json.dumps(expense_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Success", response.json())

    def test_create_expense_type(self):
        expense_type_data = {"name": "Transport"}
        response = self.client.post(reverse('create-expense-type'), json.dumps(expense_type_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Success", response.json())

    def test_create_suggestion(self):
        self.client.post(reverse('login_user'), json.dumps(self.user_data), content_type="application/json")
        suggestion_data = {
            "userID": self.user.id,
            "description": "Use LED bulbs",
            "saved_money": 20,
            "rating": 5,
            "typeID": self.suggestion_type.id
        }
        response = self.client.post(reverse('create_suggestion'), json.dumps(suggestion_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Success", response.json())

    def test_create_suggestion_type(self):
        suggestion_type_data = {"name": "Recycle"}
        response = self.client.post(reverse('create-suggestion-type'), json.dumps(suggestion_type_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Success", response.json())
