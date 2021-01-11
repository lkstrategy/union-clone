from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@unionresolute.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

def sample_client(user, name='Test Company'):
    """Create a sample client""" 
    return Client.object.create(user=user, name=name)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is success"""
        email = 'test@unionresolute.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email for a new user is normalize"""
        email = 'test@UNIONRESOLUTE.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_client_str(self):
        """Test the client string representation"""
        client = models.Client.objects.create(
            user=sample_user(),
            name='Oshyn'
        )

        self.assertEqual(str(client), client.name)

    def test_lead_str(self):
        """Test the lead string representation"""
        lead = models.Lead.objects.create(
            user=sample_user(),
            name='John'
        )

        self.assertEqual(str(lead), lead.name)

    def test_leadComplete_str(self):
        """Test the leadComplete string"""
        leadComplete = models.LeadComplete.objects.create(
            user=sample_user(),
            title='Test Company Name', 
            score=5,
            time_minutes=2.00,
            link = 'www.url.com',
            firstname = 'test first',
            client = sample_client(user=self.user, name='Test Client'),
            email = 'test@url.com',
            lastname = 'test last',
            phone = '888-66969=420',
            city = 'Northampton',
            state = 'AK',
            zipCode = '696969',
            url = 'url.com',
            linkedinLead = 'linkedin.com/lead',
            notes = 'This lead is awesome',
            salesloftId= '696969',
            )

        self.assertEqual(str(leadComplete), leadComplete.leadName)