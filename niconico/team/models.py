from django.conf import settings
from django.db import models


class Team(models.Model):
    # TODO: Create Team Owner
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        null=False,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="membership",
        through_fields=("team", "member"),
    )


class Membership(models.Model):
    # TODO: Add application status!
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
