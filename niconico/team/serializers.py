from rest_framework import serializers

from mood.serializers import UserMoodSerializer, UserSerializer
from .models import Membership, Team


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, required=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = ["id", "name", "owner", "members"]
        read_only_fields = ["id", "members"]


class TeamMoodSerializer(TeamSerializer):
    members = UserMoodSerializer(many=True)


class MembershipSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Membership(**validated_data)

    class Meta:
        model = Membership
        fields = ("team", "member")
