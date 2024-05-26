import json
from django.test import TestCase, Client
from django.urls import reverse
from api.models import CustomUser, ExpenseType, Suggestions, SuggestionType

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.expense_type = ExpenseType.objects.create(name='Food')
        self.suggestion_type = SuggestionType.objects.create(name='Savings')

    def test_register_user(self):
        url = reverse('register_user')
        data = {"username": "newuser", "password": "newpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_login_user(self):
        url = reverse('login_user')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_login_user_incorrect_password(self):
        url = reverse('login_user')
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 406)
        self.assertIn('error', response.json())

    def test_get_user(self):
        url = reverse('get_user')
        data = {"username": "testuser"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_get_user_nonexistent(self):
        url = reverse('get_user')
        data = {"username": "nonexistent"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_logout_user(self):
        self.client.session['user_id'] = self.user.id
        url = reverse('logout_user')
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_logout_user_not_logged_in(self):
        url = reverse('logout_user')
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())

    def test_delete_user(self):
        url = reverse('delete_user')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_delete_user_incorrect_password(self):
        url = reverse('delete_user')
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 406)
        self.assertIn('error', response.json())

    def test_create_expenses(self):
        self.client.session['user_id'] = self.user.id
        url = reverse('create_expenses')
        data = {
            "userID": self.user.id,
            "date": "2023-05-01",
            "amount": 100.0,
            "description": "Groceries",
            "typeName": "Food"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_suggestion(self):
        self.client.session['user_id'] = self.user.id
        url = reverse('create_suggestion')
        data = {
            "userID": self.user.id,
            "description": "Use public transport",
            "saved_money": 50.0,
            "typeName": "Savings"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    import unittest
    unittest.main()
