import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mood.serializers import MoodSerializer
from .models import Membership, MembershipStatus, Team
from .permissions import IsActiveUser
from .serializers import MembershipSerializer, TeamMoodSerializer, TeamSerializer

logger = logging.getLogger(__name__)


class TeamViewSet(viewsets.ModelViewSet):
    """Get teams for user if user is authenticated
    TODO: Allow owners to transfer ownership
    """

    paginator = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer

    @action(methods=["POST"], detail=True, url_path="join", url_name="join")
    def join_team(self, request, pk=None):
        """ Join a team
        """
        user = self.request.user
        teams = Team.objects.all()
        team = get_object_or_404(teams, pk=pk)

        # Find existing membership
        membership, created = Membership.objects.get_or_create(
            team=team, member=user, defaults={"status": MembershipStatus.PENDING.value}
        )

        # TODO: Response handling for existing case
        serializer = MembershipSerializer(membership)
        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=True,
        url_path="add_mood",
        url_name="add_mood",
        permission_classes=[IsActiveUser],
    )
    def add_mood(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        membership = get_object_or_404(Membership, member=user, team=pk)
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=user, membership=membership)
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

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Get Team overview for the membership
        TODO: Sort out architecture
        """
        user = self.request.user
        memberships = user.memberships.all()
        membership = get_object_or_404(memberships, pk=pk)
        serializer = TeamMoodSerializer(
            membership.team
        )  # TODO: Right now this returns ALL moods
        return Response(serializer.data)

    def get_queryset(self):
        memberships = Membership.objects.all()
        return memberships.filter(member=self.request.user)

    @action(methods=["PUT"], detail=True, url_path="approve", url_name="approve")
    def approve_user(self, request, pk=None):
        """ Approve a membership
        """
        user = self.request.user
        membership = get_object_or_404(Membership, pk=pk)
        if membership and membership.team.owner == user:
            membership.status = MembershipStatus.ACTIVE.value
            membership.save()
            serializer = MembershipSerializer(membership)
            return Response(serializer.data)
        return Response(data={"error": "no membership found"}, status=404)

    @action(methods=["PUT"], detail=True, url_path="suspend", url_name="suspend")
    def suspend_user(self, request, pk=None):
        """ Suspend a membership
        TODO: Refactor
        """
        user = self.request.user
        membership = get_object_or_404(Membership, pk=pk)
        if membership and membership.team.owner == user:
            membership.status = MembershipStatus.SUSPENDED.value
            membership.save()
            serializer = MembershipSerializer(membership)
            return Response(serializer.data)
        return Response(data={"error": "no membership found"}, status=404)