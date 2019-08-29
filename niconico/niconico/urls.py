from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mood.api import RegistrationAPI, LoginAPI, LogoutAPI, UserAPI
from mood.views import MoodViewSet, GetTeamView, get_mood_list
from team.views import TeamViewSet

# Create a rest framework router
router = DefaultRouter()
router.register(r"moods", MoodViewSet, base_name="Mood")
router.register(r"teamview", GetTeamView, base_name="TeamView")
router.register(r"teams", TeamViewSet, base_name="Team")

urlpatterns = [
    path("api/", include(router.urls)),
    # path("api/auth/", include("knox.urls")),
    path("api/auth/register/", RegistrationAPI.as_view()),
    path("api/auth/login/", LoginAPI.as_view(), name="knox_login"),
    path("api/auth/logout/", LogoutAPI.as_view(), name="knox_logout"),
    path("api/auth/user/", UserAPI.as_view(), name="user"),
    path("admin/", admin.site.urls),
    path("moods/", get_mood_list),
]
