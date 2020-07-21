# Django
from django.conf import settings
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from djoser import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", views.UserViewSet)

app_name = "api"
urlpatterns = [
    # Authentication (Djoser)
    path('auth/', include(router.urls)),
    re_path(r"^auth/jwt/create/?", jwt_views.TokenObtainPairView.as_view(), name="jwt-create"),

    path('dataset/', include('csv_analyzer.apps.dataset.urls_api')),
]
