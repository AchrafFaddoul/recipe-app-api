from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_user_with_email_succesful(self):
        "Test creating a new user with an email is successful"
        email = 'test@qbeast.com'
        password = 'Test@pass123++'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@QBEAST.COM'
        user = get_user_model().objects.create_user(email, 'terfvcsd@ghj')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
