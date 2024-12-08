# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_username(self):
        response = self.client.post(self.login_url, {
            'username': 'wrongusername',
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid username')

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid password')

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.logout_url, {
            'refresh': str(refresh)
        })
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)