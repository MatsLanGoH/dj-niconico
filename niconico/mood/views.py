from datetime import datetime, timedelta

import logging
from django.utils import timezone
from django.conf import settings
from django.db.models import Max, QuerySet
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import Mood, MoodChoice
from .permissions import IsOwnerOrReadOnly
from .serializers import MoodSerializer

logger = logging.getLogger(__name__)


class MoodViewSet(viewsets.ModelViewSet):
    paginator = None
    serializer_class = MoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        week = [timezone.localdate() - timedelta(days=i) for i in range(7)]

        # qs = Mood.objects.filter(created_at__gte=min(week))
        user_mood_qs = self.request.user.moods.all()
        qs = user_mood_qs.filter(created_at__gte=min(week))

        # Find missing dates and create unset moods for them
        # Hacky solution to avoid duplicate entries created for the latest date
        # TODO: Rather find a way to handle missing dates on the frontend?
        valid_days = [m.created_at.date() for m in qs]
        missing_days = [i for i, d in enumerate(week) if d not in valid_days and i > 0]

        Mood.objects.bulk_create(
            Mood(
                created_at=timezone.now() - timedelta(days=day),
                mood=MoodChoice.UNSET.value,
                message="Auto value for unset day: {}".format(day),
                owner=self.request.user,
            )
            for day in missing_days
        )

        # Retrieve last object per day
        last_per_day = (
            self.request.user.moods.all()
            .filter(created_at__gte=min(week))
            .extra(select={"date": "date(created_at)"})
            .values_list("date")
            .annotate(max_date=Max("created_at"))
        )
        last_dates = [item[1] for item in last_per_day]
        qs = self.request.user.moods.all().filter(created_at__in=last_dates)
        return qs.order_by("created_at")

