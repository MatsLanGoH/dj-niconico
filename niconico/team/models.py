from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="membership",
        through_fields=("team", "member"),
    )


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
