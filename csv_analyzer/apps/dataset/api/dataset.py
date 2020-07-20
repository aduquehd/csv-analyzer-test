from datetime import datetime

# Rest framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

# Serializers
from csv_analyzer.apps.dataset.serializers import (
    DataSetModelSerializer,
    CreateDataSetModelSerializer,
    FileDataSetModelSerializer,
)

# Models
from csv_analyzer.apps.dataset.models import DataSet

# Permissions
from csv_analyzer.apps.dataset.permissions.dataset import IsDataSetOwner

# Celery
from csv_analyzer.apps.dataset.tasks import populate_dataset_file

# MongoDB utils
from csv_analyzer.apps.mongodb.utils import MongoDBConnection


class DataSetViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsDataSetOwner)

    def get_queryset(self, *args, **kwargs):
        # Using prefetch related to improve query performance.
        return DataSet.objects.filter(owner=self.request.user).prefetch_related('files')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        data['weather_date'] = self._get_data_set_weather_data(
            from_date=request.GET.get('from_date'),
            to_date=request.GET.get('to_date'),
            data_set_id=str(instance.id)
        )

        return Response(data)

    @staticmethod
    def _get_data_set_weather_data(from_date, to_date, data_set_id):
        """
        Get a data set's weather data.
        :param from_date: String or None. Data Set from date filter. e.g. 2011-09-01
        :param to_date: String or None. Data Set to date filter. e.g. 2011-09-21
        :param data_set_id: String, Data Set Id.
        :return: Dict with count of results and the data.
        """
        mongo_client = MongoDBConnection()

        mongo_query = {
            'data_set_id': data_set_id,
        }

        if from_date or to_date:
            mongo_query['date'] = {}

            if from_date:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                from_date = datetime.combine(from_date.date(), datetime.min.time())
                mongo_query['date']['$gte'] = from_date

            if to_date:
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                to_date = datetime.combine(to_date.date(), datetime.max.time())
                mongo_query['date']['$lt'] = to_date

        files_data = mongo_client.get_list(query=mongo_query)

        return {
            'count': len(files_data),
            'data': files_data,
        }

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateDataSetModelSerializer
        elif self.action == 'add_file':
            return FileDataSetModelSerializer

        return DataSetModelSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data.update({
            'owner': request.user.id,
            'is_analyzed': False,
        })
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["POST"], url_path='add-file')
    def add_file(self, request, *args, **kwargs):
        dataset = self.get_object()

        serializer_class = self.get_serializer_class()

        try:
            data = request.data.copy()
        except Exception:
            data = request.data

        data.update({
            'data_set': dataset.id,
            'is_analyzed': False,
        })
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        populate_dataset_file.delay(dataset_file_id=serializer.instance.id)

        dataset = self.get_object()

        data = DataSetModelSerializer(dataset).data
        return Response(data=data, status=status.HTTP_201_CREATED)
