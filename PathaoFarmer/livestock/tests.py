# PathaoFarmer/livestock/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from rest_framework_simplejwt.tokens import RefreshToken

class ListLivestockOnMarketplaceTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.farm = Farm.objects.create(owner=self.user, name="Test Farm", balance=1000.00)
        self.livestock = Livestock.objects.create(farm=self.farm, type='cow', price=1000.00)
        self.list_livestock_url = reverse('list-livestock')
        self.client.login(username='testuser', password='testpassword123')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_list_livestock_on_marketplace(self):
        data = {
            'livestock_id': self.livestock.id,
            'market_price': 1500.00
        }
        response = self.client.post(self.list_livestock_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.livestock.refresh_from_db()
        self.assertTrue(self.livestock.is_listed)
        self.assertEqual(self.livestock.market_price, 1500.00)

    def test_get_all_marketplace_livestock(self):
        # List the livestock on the marketplace first
        self.livestock.is_listed = True
        self.livestock.market_price = 1500.00
        self.livestock.save()

        response = self.client.get(self.list_livestock_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.livestock.id)
        self.assertEqual(response.data[0]['market_price'], '1500.00')