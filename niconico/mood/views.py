from datetime import datetime, timedelta
from django.db.models import Max, QuerySet
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from mood.models import Mood, MoodChoice
from mood.serializers import MoodSerializer


class MoodViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        week = [datetime.now().date() + timedelta(days=-7 + i) for i in range(8)]
        valid_days = []
        for day in week:
            qs = Mood.objects.filter(created_at__date=day)
            if qs:
                valid_days.append(qs.latest("created_at").id)
            else:
                # Create empty object for that date
                unset = Mood.objects.create(created_at=day, mood=MoodChoice.UNSET.value)
                valid_days.append(unset.id)
        return Mood.objects.filter(id__in=valid_days).order_by("created_at")

    # Get days for the past week
    paginator = None
    serializer_class = MoodSerializer
