from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from transactions.models import Transaction
from rest_framework_simplejwt.tokens import RefreshToken

class PurchaseLivestockTests(APITestCase):

    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='testpassword123', email='buyer@example.com')
        self.seller = User.objects.create_user(username='seller', password='testpassword123', email='seller@example.com')
        self.buyer_farm = Farm.objects.create(owner=self.buyer, name="Buyer's Farm", balance=2000.00)
        self.seller_farm = Farm.objects.create(owner=self.seller, name="Seller's Farm", balance=1000.00)
        self.livestock = Livestock.objects.create(farm=self.seller_farm, type='cow', price=1000.00, market_price=1500.00, is_listed=True)
        self.purchase_url = reverse('purchase-livestock')
        self.transaction_history_url = reverse('transaction-history')
        self.client.login(username='buyer', password='testpassword123')
        self.token = RefreshToken.for_user(self.buyer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_purchase_livestock(self):
        data = {
            'livestock_id': self.livestock.id
        }
        response = self.client.post(self.purchase_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.livestock.refresh_from_db()
        self.buyer_farm.refresh_from_db()
        self.seller_farm.refresh_from_db()
        self.assertFalse(self.livestock.is_listed)
        self.assertEqual(self.livestock.farm.owner, self.buyer)
        self.assertEqual(self.buyer_farm.balance, 500.00)
        self.assertEqual(self.seller_farm.balance, 2500.00)

    def test_transaction_history(self):
        # Perform a purchase first
        data = {
            'livestock_id': self.livestock.id
        }
        self.client.post(self.purchase_url, data)

        # Get transaction history
        response = self.client.get(self.transaction_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        transaction = response.data[0]

        self.assertEqual(transaction['buyer']['username'], self.buyer.username)
        self.assertEqual(transaction['seller']['username'], self.seller.username)
        self.assertEqual(transaction['livestock']['type'], self.livestock.type)
        self.assertEqual(transaction['selling_price'], '1500.00')