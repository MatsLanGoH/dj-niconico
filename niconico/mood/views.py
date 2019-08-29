import logging
from datetime import timedelta

from django.db.models import Max
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from team.models import Membership, Team
from .models import Mood, MoodChoice
from .serializers import MoodSerializer

logger = logging.getLogger(__name__)


class MoodViewSet(viewsets.ModelViewSet):
    paginator = None
    serializer_class = MoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        week = [
            timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
            - timedelta(days=i + 1)
            for i in range(31)
        ]

        # qs = Mood.objects.filter(created_at__gte=min(week))
        user_mood_qs = self.request.user.moods.filter(membership__isnull=True)
        qs = user_mood_qs.filter(created_at__gte=min(week))

        # Find missing dates and create unset moods instances for them
        # TODO: Rather find a way to handle missing dates on the frontend?
        valid_days = [m.created_at.date() for m in qs]
        missing_days = [
            i for i, d in enumerate(week) if d.date() not in valid_days and i > 0
        ]

        # Create filler instances
        unset_moods = [
            Mood(
                created_at=timezone.localtime() - timedelta(days=day),
                mood=MoodChoice.UNSET.value,
                message="Auto value for unset day: {}".format(day),
                owner=self.request.user,
            )
            for day in missing_days
        ]

        # Retrieve last object per day
        last_per_day = (
            self.request.user.moods.filter(membership__isnull=True)
            .filter(created_at__gte=min(week))
            .extra(
                select={"date": "date(created_at, '+9 hours')"}
            )  # Adjust for JST timezone
            .values_list("date")
            .annotate(max_date=Max("created_at"))
        )
        last_dates = [item[1] for item in last_per_day]
        qs = self.request.user.moods.filter(membership__isnull=True).filter(
            created_at__in=last_dates
        )

        # Combine actual Moods with filler instances, sort by date and return
        combined_moods = sorted(list(qs) + unset_moods, key=lambda m: m.created_at)
        return combined_moods


class GetTeamView(viewsets.ReadOnlyModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # TODO: Get Team from somewhere
        team = 1
        qs = self.request.user.teams.filter(pk=team)
        breakpoint()
        return qs


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_mood_list(request):
    """List all moods
    """
    moods = Mood.objects.all()
    serializer = MoodSerializer(moods, many=True)
    return Response(serializer.data)


class GetMembershipView(viewsets.ReadOnlyModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # TODO: Get Team from somewhere
        # Returns all moods for a given membership
        membership = Membership.objects.filter(
            member=self.request.user, team=Team.objects.first()
        ).first()

        qs = Mood.objects.filter(membership=membership)
        return qs
