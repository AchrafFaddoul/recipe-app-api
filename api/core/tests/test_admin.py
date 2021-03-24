from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@qbeast.com',
            password='test@13334+++'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@qbeast.com',
            password='pass@word123++',
            name='Achraf Faddoul'
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        """"assertContains check if res status code is 200 &\
            second specified arg is exist"""
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
