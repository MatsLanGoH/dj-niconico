from rest_framework import serializers

from .models import Mood


class MoodSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    timestamp = serializers.SerializerMethodField("get_timestamp")

    def get_timestamp(self, obj):
        return obj.created_at.timestamp()

    class Meta:
        model = Mood
        fields = ("id", "mood", "message", "created_at", "timestamp", "created_by")
