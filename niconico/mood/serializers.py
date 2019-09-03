from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from rest_framework import serializers

from team.models import MembershipStatus
from .models import Mood


class MoodSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # id = serializers.ReadOnlyField()
    # mood = serializers.ReadOnlyField()
    # message = serializers.ReadOnlyField()
    # created_at = serializers.DateTimeField()
    team = serializers.IntegerField(source="membership.team_id", required=False)
    timestamp = serializers.SerializerMethodField(required=False)
    date = serializers.SerializerMethodField(required=False)

    def get_timestamp(self, obj):
        if obj.created_at:
            return obj.created_at.timestamp()
        return None

    def get_date(self, obj):
        return localtime(obj.created_at).date() or None

    class Meta:
        model = Mood
        fields = (
            "id",
            "mood",
            "message",
            "created_at",
            "timestamp",
            "owner",
            "team",
            "date",
        )


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
    class Meta:
        model = User
        fields = ("id", "username")


class UserStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        membership = obj.memberships.filter(team_id=self.context["team"].id).first()
        return membership.get_status_display()

    class Meta:
        model = User
        fields = ("id", "username", "status")


class UserMoodSerializer(serializers.ModelSerializer):
    moods = MoodSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "moods")


class UserMoodExtraSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    moods = serializers.SerializerMethodField()

    def get_status(self, obj):
        membership = obj.memberships.filter(team_id=self.context["team"].id).first()
        return membership.get_status_display()

    def get_moods(self, obj):
        return MoodSerializer(
            # TODO:  use repository instead
            obj.moods.filter(
                membership__team=self.context["team"].id,
                membership__status=MembershipStatus.ACTIVE.value,
            ),
            read_only=True,
            many=True,
        ).data

    class Meta:
        model = User
        fields = ("id", "username", "status", "moods")
        read_only_fields = ("id", "username", "status", "moods")
