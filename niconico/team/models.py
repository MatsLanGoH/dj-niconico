from django.conf import settings
from django.db import models


class Team(models.Model):
    # TODO: Create Team Owner
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


class Membership(models.Model):
    # TODO: Add application status!
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="memberships", on_delete=models.CASCADE
    )

    def __str__(self):
        as_string = f"ID: {self.id}, Team: {self.team_id}: {self.team}, Member: {self.member_id}: {self.member}"
        return as_string
