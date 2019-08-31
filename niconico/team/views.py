import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import Membership
from .serializers import MembershipSerializer, TeamMoodSerializer, TeamSerializer

logger = logging.getLogger(__name__)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """Get teams for user if user is authenticated
    """

    paginator = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Team detail view
        """
        user = self.request.user
        teams = user.teams.all()
        team = get_object_or_404(teams, pk=pk)

        # TODO: Can we group these by dates??
        serializer = TeamMoodSerializer(team)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return user.teams.all()


class MembershipViewSet(viewsets.ReadOnlyModelViewSet):
    """Get memberships for user if authenticated
    """

    paginator = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembershipSerializer

    def get_queryset(self):
        memberships = Membership.objects.all()
        return memberships.filter(member=self.request.user)
