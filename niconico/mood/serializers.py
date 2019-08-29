from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from rest_framework import serializers

from .models import Mood


class MoodSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # id = serializers.ReadOnlyField()
    # mood = serializers.ReadOnlyField()
    # message = serializers.ReadOnlyField()
    # created_at = serializers.DateTimeField()
    timestamp = serializers.SerializerMethodField("get_timestamp", required=False)
    date = serializers.SerializerMethodField("get_date", required=False)

    def get_timestamp(self, obj):
        if obj.created_at:
            return obj.created_at.timestamp()
        return None

    def get_date(self, obj):
        return localtime(obj.created_at).date() or None

    class Meta:
        model = Mood
        fields = ("id", "mood", "message", "created_at", "timestamp", "owner", "date")


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


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class UserSerializer(serializers.ModelSerializer):
    moods = MoodSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "moods")
