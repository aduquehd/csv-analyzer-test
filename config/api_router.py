# Django
from django.conf import settings
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = [
    # Authentication (Djoser)
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),

    path('dataset/', include('csv_analyzer.apps.dataset.urls_api')),

]
