import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Membership, Team
from .serializers import MembershipSerializer, TeamSerializer

logger = logging.getLogger(__name__)


class TeamViewSet(viewsets.ModelViewSet):
    """Get teams for user if user is authenticated
    TODO: Allow owners to transfer ownership
    TODO: Use "TeamRelations" (MembershipTeams) to allow users to see
         teams of which they are members of
    """

    paginator = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer

    @action(methods=["POST"], detail=True, url_path="join-team", url_name="join-team")
    def join_team(self, request, pk=None):
        """ Join a team
        TODO: Set join status to probational status
        """
        user = self.request.user
        teams = Team.objects.all()
        team = get_object_or_404(teams, pk=pk)
        membership = Membership(team=team, member=user)
        membership.save()

        serializer = MembershipSerializer(membership)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.managed_teams.all()


class MembershipViewSet(viewsets.ReadOnlyModelViewSet):
    """Get memberships for user if authenticated
    """

    paginator = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembershipSerializer

    def get_queryset(self):
        memberships = Membership.objects.all()
        return memberships.filter(member=self.request.user)
