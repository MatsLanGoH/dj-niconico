from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mood import views
from mood.api import RegistrationAPI, LoginAPI, LogoutAPI, UserAPI

# Create a rest framework router
router = DefaultRouter()
router.register(r"moods", views.MoodViewSet, base_name="Mood")

urlpatterns = [
    path("api/", include(router.urls)),
    # path("api/auth/", include("knox.urls")),
    path("api/auth/register/", RegistrationAPI.as_view()),
    path("api/auth/login/", LoginAPI.as_view(), name="knox_login"),
    path("api/auth/logout/", LogoutAPI.as_view(), name="knox_logout"),
    path("api/auth/user/", UserAPI.as_view(), name="user"),
    path("admin/", admin.site.urls),
]
