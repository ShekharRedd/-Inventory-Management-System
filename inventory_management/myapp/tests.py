# tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item

class ItemTests(APITestCase):

    def setUp(self):
        # Create a test item
        self.item = Item.objects.create(
            name="Test Item",
            description="A test item",
            quantity=5,
            price=100
        )
        # Use token authentication if needed
        self.token = "your_token"

    def test_read_item_success(self):
        # Test retrieving an existing item
        url = reverse('read_item', kwargs={'item_id': self.item.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_read_item_not_found(self):
        # Test retrieving a non-existing item
        url = reverse('read_item', kwargs={'item_id': 9999})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Item not found")

    def test_update_item(self):
        # Test updating an item
        url = reverse('update_item', kwargs={'item_id': self.item.id})
        data = {
            'name': 'Updated Item',
            'description': 'Updated description',
            'quantity': 10,
            'price': 150
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Item updated successfully')

    def test_delete_item(self):
        # Test deleting an item
        url = reverse('delete_item', kwargs={'item_id': self.item.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Item deleted successfully')
