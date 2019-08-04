from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings
from django.db.models import Max, QuerySet
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from mood.models import Mood, MoodChoice
from mood.serializers import MoodSerializer


class MoodViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        week = [timezone.now() - timedelta(days=i) for i in range(7)]
        week_dates = [d.date() for d in week]
        qs = Mood.objects.filter(created_at__gte=min(week_dates))

        # Find missing dates and create unset moods for them
        # TODO: Rather find a way to handle missing dates on the frontend?
        valid_days = [m.created_at.date() + timedelta(days=1) for m in qs]
        missing_days = [d for d in week_dates if d not in valid_days]

        Mood.objects.bulk_create(
            Mood(created_at=day, mood=MoodChoice.UNSET.value) for day in missing_days
        )

        # Retrieve objects once again :(
        qs = Mood.objects.filter(created_at__gte=min(week_dates))
        return qs.order_by("created_at")

    # Get days for the past week
    paginator = None
    serializer_class = MoodSerializer
