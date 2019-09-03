import logging

from rest_framework import permissions, viewsets

from .models import Membership
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
