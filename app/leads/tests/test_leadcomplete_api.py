from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import LeadComplete, Client, Lead

from leads.serializers import LeadCompleteSerializer, LeadCompleteDetailSerializer

LEADCOMPLETE_URL = reverse('leads:leadcomplete-list')
#/api/leads/leadcomplete
#/api/leads/leadcomplete/1

def detail_url(leadComplete_id):
    """Return lead complete detail URL"""
    return reverse('leads:leadcomplete-detail', args=[leadComplete_id])

def sample_lead(user, name='Test Company'):
    """Create a sample lead"""
    return Lead.objects.create(user=user, name=name)

def sample_client(user, name='Company XYZ'):
    """Create and return sample Client"""
    return Client.objects.create(user=user, name=name)


def sample_leadComplete(user, **params):
    """Create and return a sample leadComplete"""
    defaults = {
        'title': 'Samle Company',
        'time_minutes': 10,
        'score': 5.00,
    }
    defaults.update(params)

    return LeadComplete.objects.create(user=user, **defaults)

def PublicLeadCompleteApiTests(TestCase):
    """Test unauthenticated LeacComplete access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """"Test that authentication is required"""
        res = selft.client.get(LEADCOMPLETE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateLeadCompleteApiTests(TestCase):
    """"Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@unionresolute.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_leadComplete(self):
        """Test retrieving LeadComplete list"""
        sample_leadComplete(user=self.user)
        sample_leadComplete(user=self.user)

        res = self.client.get(LEADCOMPLETE_URL)

        leadComplete = LeadComplete.objects.all().order_by('-id')
        serializer = LeadCompleteSerializer(leadComplete, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_leadComplete_limited_to_user(self):
        """Test retrieving leadComplete for user"""
        user2 = get_user_model().objects.create_user(
            'other@unionresolute.com',
            'password123'
        )
        sample_leadComplete(user=user2)
        sample_leadComplete(user=self.user)

        res = self.client.get(LEADCOMPLETE_URL)

        leadComplete = LeadComplete.objects.filter(user=self.user)
        serializer = LeadCompleteSerializer(leadComplete, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_leadComplete_view_detail(self):
        """Test viewing a leadComplete detail"""
        leadComplete = sample_leadComplete(user=self.user)
        leadComplete.client.add(sample_client(user=self.user))

        url = detail_url(leadComplete.id)
        res = self.client.get(url)

        serializer = LeadCompleteDetailSerializer(leadComplete)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_leadComplete(self):
        """Test creating LeadComplete"""
        payload = {
            'title': 'Sample Company',
            'time_minutes': 40,
            'score': 7.00
        }
        res = self.client.post(LEADCOMPLETE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        leadComplete = LeadComplete.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(leadComplete, key))

    def test_create_leadComplete_with_client(self):
        """Test creating leadComplete with client"""
        client1 = sample_client(user=self.user, name='Super Acme')
        payload = {
            'title': 'Sample Company',
            'client': [client1.id,],
            'time_minutes':40,
            'score':7.00
        }    
        res = self.client.post(LEADCOMPLETE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        leadComplete = LeadComplete.objects.get(id=res.data['id'])
        client = leadComplete.client.all()
        self.assertEqual(client.count(), 1)
        self.assertIn(client1, client)

    def test_filter_leadComplete_by_client(self):
        """Test returning leadcomplete from specific client"""
        leadComplete1 = sample_leadComplete(user=self.user, title='Sample company')
        leadComplete2 = sample_leadComplete(user=self.user, title='Tesst company')
        client1 = sample_client(user=self.user, name='Test Client')
        client2 = sample_client(user=self.user, name='Sample Client')
        leadComplete1.client.add(client1)
        leadComplete2.client.add(client2)
        leadComplete3 = sample_leadComplete(user=self.user, title='Super Test Co')

        res = self.client.get(
            LEADCOMPLETE_URL,
            {'client': f'{client1.id},{client2.id}'}
        )

        serializer1 = LeadCompleteSerializer(leadComplete1)
        serializer2 = LeadCompleteSerializer(leadComplete2)
        serializer3 = LeadCompleteSerializer(leadComplete3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)






    