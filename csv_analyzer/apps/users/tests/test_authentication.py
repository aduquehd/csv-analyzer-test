from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from csv_analyzer.apps.users.models import User
from csv_analyzer.apps.users.tests.factories import UserFactory


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.sign_up_url = "/api/auth/users/"
        self.login_url = "/api/auth/jwt/create/"
        UserFactory()
        user = User.objects.get()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_create_user(self):
        data = {
            "username": "test1@mail.com",
            "password": "abcd1234."
        }
        response = self.client.post(self.sign_up_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "test1@mail.com")
        self.assertTrue('id' in response.data)
        self.assertTrue(User.objects.filter(username='test1@mail.com').exists())

    def test_login(self):
        u = User.objects.get()
        u.set_password("some-secure-password.123")
        u.save()

        data = {
            "username": u.username,
            "password": "some-secure-password.123"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_login_wrong_user(self):
        u = User.objects.get()
        u.set_password("some-secure-password.123")
        u.save()

        data = {
            "username": u.username,
            "password": "some-wrong-password.123"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "No active account found with the given credentials")
        self.assertFalse('access' in response.data)
        self.assertFalse('refresh' in response.data)
