from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient 

from core.models import Lead

from leads.serializers import LeadSerializer

LEADS_URL = reverse('leads:lead-list')

class PublicLeadsApiTest(TestCase):
    """The the publicly available leads api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required to access endpoint"""
        res = self.client.get(LEADS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateLeadsApiTests(TestCase):
    """Test leads can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@unionresolute.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieve a list of leads"""
        Lead.objects.create(user=self.user, name='Smith')
        Lead.objects.create(user=self.user, name='Joe')

        res=self.client.get(LEADS_URL)

        leads = Lead.objects.all().order_by('-name')
        serializer = LeadSerializer(leads, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_leads_limited_to_user(self):
        """Test that leads for authenticated user are return"""
        user2 = get_user_model().objects.create_user(
            'other@unionresolute.com',
            'testpass'
        )
        Lead.objects.create(user=user2, name='Joe')
        lead = Lead.objects.create(user=self.user, name='John')

        res = self.client.get(LEADS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], lead.name)

    def test_create_lead_successful(self):
        """Test ccreate a new ingredient"""
        payload = {'name': 'Joe'}
        self.client.post(LEADS_URL, payload)

        exists = Lead.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_lead_invalid(self):
        payload = {'name': ''}
        self.client.post(LEADS_URL, payload)
        res = self.client.post(LEADS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


