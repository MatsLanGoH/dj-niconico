from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mood.api import LoginAPI, LogoutAPI, RegistrationAPI, UserAPI
from mood.views import MoodViewSet
from team.views import MembershipViewSet, TeamViewSet

# Create a rest framework router
router = DefaultRouter()
router.register(r"moods", MoodViewSet, base_name="mood")
router.register(r"memberships", MembershipViewSet, base_name="membership")
router.register(r"teams", TeamViewSet, base_name="team")

urlpatterns = [
    path("api/", include(router.urls)),
    # path("api/auth/", include("knox.urls")),
    path("api/auth/register/", RegistrationAPI.as_view()),
    path("api/auth/login/", LoginAPI.as_view(), name="knox_login"),
    path("api/auth/logout/", LogoutAPI.as_view(), name="knox_logout"),
    path("api/auth/user/", UserAPI.as_view(), name="user"),
    path("admin/", admin.site.urls),
]
