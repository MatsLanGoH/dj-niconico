from django.db.models import Max
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from mood.models import Mood
from mood.serializers import MoodSerializer


class MoodViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    paginator = None
    serializer_class = MoodSerializer

