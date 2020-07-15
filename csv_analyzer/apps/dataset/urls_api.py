# Django
from django.conf import settings
from django.urls import include, path

# Importing Django rest libraries.
from rest_framework.routers import DefaultRouter, SimpleRouter

# Views
from csv_analyzer.apps.dataset.api.dataset import DataSetViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", DataSetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls))
]
