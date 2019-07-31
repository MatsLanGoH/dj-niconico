from enum import Enum, auto
from django.conf import settings
from django.db import models


# Define possible mood choices
class MoodChoice(Enum):
    HAPPY = auto()
    NEUTRAL = auto()
    SAD = auto()


class Mood(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mood = models.IntegerField(choices=[(tag.value, tag.name) for tag in MoodChoice])
    message = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )
