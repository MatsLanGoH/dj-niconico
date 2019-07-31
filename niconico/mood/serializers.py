from rest_framework import serializers

from .models import Mood


class MoodSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Mood
        fields = ("id", "mood", "message", "created_at", "created_by")
