from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Item

User = get_user_model()  # This will get the User model correctly

class ItemTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Description',
            quantity=10,
            price=100.0
        )
        self.token = self.get_token()

    def get_token(self):
        # Obtain token by logging in
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        return response.data['access']  # Adjust if your response structure is different

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_item_success(self):
        self.authenticate()
        response = self.client.post(reverse('create_item'), {
            'name': 'New Item',
            'description': 'New Description',
            'quantity': 5,
            'price': 50.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item_success(self):
        self.authenticate()
        response = self.client.get(reverse('read_item', kwargs={'item_id': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_read_item_not_found(self):
        self.authenticate()
        response = self.client.get(reverse('read_item', kwargs={'item_id': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        self.authenticate()
        response = self.client.put(reverse('update_item', kwargs={'item_id': self.item.id}), {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'quantity': 20,
            'price': 150.0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')

    def test_delete_item(self):
        self.authenticate()
        response = self.client.delete(reverse('delete_item', kwargs={'item_id': self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.filter(id=self.item.id).count(), 0)
