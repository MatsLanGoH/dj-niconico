from rest_framework import serializers

from mood.serializers import UserMoodExtraSerializer, UserSerializer
from .models import Membership, Team


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, required=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = ["id", "name", "owner", "members"]
        read_only_fields = ["id", "members"]


class TeamMoodSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(source="get_members")

    def get_members(self, obj):
        return UserMoodExtraSerializer(
            obj.members.all(), many=True, read_only=True, context={"membership": obj}
        ).data

    class Meta:
        model = Team
        fields = ["id", "name", "owner", "members"]
        read_only_fields = ["id", "members"]


class MembershipSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")

    def create(self, validated_data):
        return Membership(**validated_data)

    class Meta:
        model = Membership
        fields = ("id", "team", "member", "status")
