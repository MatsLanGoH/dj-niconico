from enum import Enum, auto
from django.conf import settings
from django.db import models
from django.utils import timezone

from team.models import Membership


# Define possible mood choices
class MoodChoice(Enum):
    HAPPY = auto()
    NEUTRAL = auto()
    SAD = auto()
    UNSET = auto()


class Mood(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    mood = models.IntegerField(choices=[(tag.value, tag.name) for tag in MoodChoice])
    message = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="moods",
        null=True,
        on_delete=models.CASCADE,
    )
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'<{self.pk}><{self.created_at}> {MoodChoice(self.mood).name} "{self.message}"'
