from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_verify')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email':'test@xyz.com',
            'password':'passtest123',
            'name':'test',
        }

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            'email':'test@xyz.com',
            'password':'passtest123',
            'name':'test',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email':'test@xyz.com',
            'password':'p3',
            'name':'test',
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # def test_create_token_for_user(self):
    #     user_details = {
    #         'name':'test name',
    #         'email':'test@xyz.com',
    #         'password':'testpass123',
    #     }
    #     create_user(**user_details)

    #     payload = {
    #         'email':user_details['email'],
    #         'password':user_details['password'],
    #     }
    #     res =self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token',res.data)
    #     self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    # def test_create_token_bad_credentials(self):
    #     """Test returns error if credentials invalid."""
    #     create_user(email='test@example.com', password='goodpass')

    #     payload = {
    #         'email': 'test@example.com',
    #         'password': 'badpass',
    #         }
    #     res = self.client.post(TOKEN_URL, payload)


    #     self.assertNotIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    # def test_create_token_email_not_found(self):
    #     """Test error returned if user not found for given email."""
    #     payload = {
    #         'email': 'test@example.com',
    #         'password': 'pass123',
    #         }
    #     res = self.client.post(TOKEN_URL, payload)
    #     self.assertNotIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_token_blank_password(self):
    #     """Test posting a blank password returns an error."""
    #     payload = {'email': 'test@example.com', 'password': ''}
    #     res = self.client.post(TOKEN_URL, payload)
    #     self.assertNotIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)