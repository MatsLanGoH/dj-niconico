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
        week = [timezone.localdate() - timedelta(days=i) for i in range(7)]

        qs = Mood.objects.filter(created_at__gte=min(week))

        # Find missing dates and create unset moods for them
        # TODO: Rather find a way to handle missing dates on the frontend?
        valid_days = [m.created_at.date() for m in qs]
        missing_days = [d for d in week if d not in valid_days]

        Mood.objects.bulk_create(
            Mood(
                created_at=day,
                mood=MoodChoice.UNSET.value,
                message="Auto value for unset day: {}".format(day),
            )
            for day in missing_days
        )

        # Retrieve last object per day
        last_per_day = (
            Mood.objects.filter(created_at__gte=min(week))
            .extra(select={"date": "date(created_at)"})
            .values_list("date")
            .annotate(max_date=Max("created_at"))
        )
        last_dates = [item[1] for item in last_per_day]
        qs = Mood.objects.filter(created_at__in=last_dates)
        return qs.order_by("created_at")

    # Get days for the past week
    paginator = None
    serializer_class = MoodSerializer
