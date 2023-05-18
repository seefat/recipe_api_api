from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@xyz.com',
            password = 'admin123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'user@xyz.com',
            password = 'user123',
            name = 'user name',
        )

    def test_user_lists(self):
        url = reverse('admin:test_app_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        url = reverse('admin:test_app_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        url = reverse('admin:test_app_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)