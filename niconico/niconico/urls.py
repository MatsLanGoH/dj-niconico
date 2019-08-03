from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mood import views

# Create a rest framework router
router = DefaultRouter()
router.register(r"moods", views.MoodViewSet, base_name="Mood")

urlpatterns = [path("api/", include(router.urls)), path("admin/", admin.site.urls)]
