from enum import Enum, auto

from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_teams",
        null=False,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        through="membership",
        through_fields=("team", "member"),
    )

    def __str__(self):
        as_string = f"ID: {self.id}: {self.name}, Owner: {self.owner_id}: {self.owner}, Members: {self.members}"
        return as_string


class MembershipStatus(Enum):
    PENDING = auto()  # New members (need to be approved)
    ACTIVE = auto()  # Active (after approval)
    SUSPENDED = auto()  # Suspended (in case admin suspends)


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="memberships", on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in MembershipStatus]
    )

    def __str__(self):
        as_string = (
            f"ID: {self.id}, Team: {self.team_id}, "
            f"Member: {self.member_id}: {self.member} ({self.get_status_display()})"
        )
        return as_string
