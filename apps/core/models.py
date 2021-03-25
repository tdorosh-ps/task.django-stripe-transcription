from django.db import models
from django.contrib.auth.models import AbstractUser

from .exceptions import NegativeAmountError, NotEnoughTranscriptionsError


class User(AbstractUser):
    transcriptions_count = models.PositiveSmallIntegerField(default=3)

    def increment_transcriptions_count(self, amount):
        if not isinstance(amount, int):
            raise TypeError('Pass integer as amount')
        if amount <= 0:
            raise NegativeAmountError('Pass integer value more than 0')
        self.transcriptions_count += amount

    def decrement_transcriptions_count(self, amount):
        if not isinstance(amount, int):
            raise TypeError('Pass integer as amount')
        if amount <= 0:
            raise NegativeAmountError('Pass integer value more than 0')
        if self.transcriptions_count < amount:
            raise NotEnoughTranscriptionsError('Not enough transcriptions')
        self.transcriptions_count -= amount


class UserTeam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='own_teams')
    users = models.ManyToManyField(User, related_name='teams')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
