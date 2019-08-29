from rest_framework import serializers

from mood.serializers import UserSerializer
from .models import Team, Membership


class TeamSerializer(serializers.ModelSerializer):
    # members = serializers.StringRelatedField(many=True)
    members = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = ("name", "owner", "members")


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ("team", "member")
