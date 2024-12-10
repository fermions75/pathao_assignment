# PathaoFarmer/farmers/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from rest_framework_simplejwt.tokens import RefreshToken

class FarmerDetailsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.farm = Farm.objects.create(owner=self.user, name="Test Farm", balance=1000.00)
        Livestock.objects.create(farm=self.farm, type='cow', price=1000.00)
        Livestock.objects.create(farm=self.farm, type='goat', price=800.00)
        Livestock.objects.create(farm=self.farm, type='sheep', price=500.00)
        self.url = reverse('farmer-details')
        self.client.login(username='testuser', password='testpassword123')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_get_farmer_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['farm']['name'], self.farm.name)
        self.assertEqual(len(response.data['farm']['livestock']), 3)
        livestock_types = [livestock['type'] for livestock in response.data['farm']['livestock']]
        self.assertIn('cow', livestock_types)
        self.assertIn('goat', livestock_types)
        self.assertIn('sheep', livestock_types)