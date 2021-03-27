from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


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
        payload = {'email': 'test@qbeast.com', 'password': 'testpass@1'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test@qbeast.com', 'password': 'tst'}

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
