from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Client

from leads.serializers import ClientSerializer

CLIENTS_URL = reverse('leads:client-list')

class PublicClientsApiTests(TestCase):
    """Test the publicly available clients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(CLIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateClientsApiTests(TestCase):
    """Tests the authorized use Clients API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@unionresolute.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_clients(self):
        """Test retriving clients"""
        Client.objects.create(user=self.user, name='Fake LLC')
        Client.objects.create(user=self.user, name='Test LLC')

        res = self.client.get(CLIENTS_URL)

        clients = Client.objects.all().order_by('-name')
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_clients_limited_to_user(self):
        """Test that clients are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@unionresolute.com',
            'testpass'
        )
        Client.objects.create(user=user2, name='sillytest')
        client = Client.objects.create(user=self.user, name='bland inc')

        res = self.client.get(CLIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], client.name)

    def test_create_client_succesful(self):
        """Test creating a new client"""
        payload = {'name': 'Test LLC'}
        self.client.post(CLIENTS_URL, payload)

        exists = Client.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(CLIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


