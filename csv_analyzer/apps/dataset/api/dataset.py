# Rest framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Serializers
from csv_analyzer.apps.dataset.serializers import (
    DataSetModelSerializer,
    CreateDataSetModelSerializer,
    FileDataSetModelSerializer,
)

# Models
from csv_analyzer.apps.dataset.models import DataSet

# Celery
from csv_analyzer.apps.dataset.tasks import populate_dataset_file

# MongoDB utils
from csv_analyzer.apps.mongodb.utils import MongoDBConnection


class DataSetViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

    def get_queryset(self, *args, **kwargs):
        # Using prefetch related to improve query performance.
        return DataSet.objects.filter(owner=self.request.user).prefetch_related('files')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        mongo_client = MongoDBConnection()
        files_data = mongo_client.get_list(query={'data_set_id': str(instance.id)})
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['all_data'] = files_data
        return Response(data)

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
