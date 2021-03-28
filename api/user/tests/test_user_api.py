from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import FakePayload
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@qbeast.com',
            'password': 'testpass@1',
            'name': 'Q Beast'
        }
        # create user
        res = self.client.post(CREATE_USER_URL, payload)

        # status code if 201 CREATED
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get created user
        user = get_user_model().objects.get(**res.data)
        # check if pwd of created user is the same in the payload
        self.assertTrue(user.check_password(payload['password']))
        # check if pwd not included in response data
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'test@qbeast.com',
            'password': 'testpass@1',
            'name': 'Test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@qbeast.com',
            'password': 'tst',
            'name': 'Test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@qbeast.com',
            'password': 'tst',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.status.HTTP_200_OK)

    def test_create_token_invalid_crendentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@qbeast.com', password='testpass')
        payload = {
            'email': 'test@qbeast.com',
            'password': 'teeest#@@!24Wrong',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'test@qbeast.com',
            'password': 'Test@123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
