from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from csv_analyzer.apps.users.models import User
from csv_analyzer.apps.dataset.models import DataSet
from csv_analyzer.apps.users.tests.factories import UserFactory


class DataSetTest(APITestCase):
    def setUp(self):
        self.url = "/api/dataset/"
        UserFactory()
        user = User.objects.get()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_create_dataset_duplicated_name(self):
        data = {
            "name": "Dataset N1",
        }
        user = User.objects.get()
        DataSet.objects.create(
            name="Dataset N1",
            owner=user
        )

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "The fields name, owner must make a unique set.")

    def test_create_dataset(self):
        data = {
            "name": "Dataset N2",
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Dataset N2")
