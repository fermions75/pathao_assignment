from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com'
        }

    def test_register(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertTrue(Farm.objects.filter(owner__username=self.user_data['username']).exists())
        farm = Farm.objects.get(owner__username=self.user_data['username'])
        self.assertEqual(farm.livestock.filter(type='cow').count(), 5)
        self.assertEqual(farm.livestock.filter(type='goat').count(), 5)
        self.assertEqual(farm.livestock.filter(type='sheep').count(), 3)

    def test_login(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_username(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'wrongusername',
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid username')

    def test_login_invalid_password(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid password')

    def test_logout(self):
        # Register the user first
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh = response.data['refresh']
        response = self.client.post(self.logout_url, {
            'refresh': refresh
        })
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)