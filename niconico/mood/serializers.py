from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Mood


class MoodSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # id = serializers.ReadOnlyField()
    # mood = serializers.ReadOnlyField()
    # message = serializers.ReadOnlyField()
    # created_at = serializers.DateTimeField()
    timestamp = serializers.SerializerMethodField("get_timestamp")

    def get_timestamp(self, obj):
        return obj.created_at.timestamp()

    class Meta:
        model = Mood
        fields = ("id", "mood", "message", "created_at", "timestamp", "owner")


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
