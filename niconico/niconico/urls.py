from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mood import views
from mood.api import RegistrationAPI

# Create a rest framework router
router = DefaultRouter()
router.register(r"moods", views.MoodViewSet, base_name="Mood")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/", include("knox.urls")),
    path("api/auth/register/", RegistrationAPI.as_view()),
    path("admin/", admin.site.urls),
]
