from rest_framework import serializers

from mood.serializers import UserMoodSerializer, UserSerializer
from .models import Membership, Team


class TeamSerializer(serializers.ModelSerializer):
    # members = serializers.StringRelatedField(many=True)
    members = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "owner", "members")


class TeamMoodSerializer(TeamSerializer):
    members = UserMoodSerializer(many=True)


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ("team", "member")
