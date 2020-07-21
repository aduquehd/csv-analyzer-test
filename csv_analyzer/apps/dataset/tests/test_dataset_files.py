from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from csv_analyzer.apps.users.models import User
from csv_analyzer.apps.dataset.models import DataSet, DataSetFiles
from csv_analyzer.apps.users.tests.factories import UserFactory


class DataSetFileTest(APITestCase):
    def setUp(self):
        self.url = "/api/dataset/"
        UserFactory()
        user = User.objects.get()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_create_dataset_file(self):
        user = User.objects.get()
        dataset = DataSet.objects.create(name="Dataset N2", owner=user)

        url = f"{self.url}{str(dataset.id)}/add-file/"

        with open("csv_analyzer/apps/dataset/tests/files/daily_weather_test.xlsx", 'rb') as fp:
            post_data = {
                'file': fp,
                'start_date': "2011-09-01",
            }
            response = self.client.post(url, post_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Dataset N2")
        self.assertEqual(len(response.data['files']), 1)
        self.assertEqual(DataSetFiles.objects.filter(data_set=dataset).count(), 1)
