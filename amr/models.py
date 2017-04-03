from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AmrEntry(models.Model):
    sentence = models.CharField(max_length=1000)
    amr = models.CharField(max_length=5000)


class Generation(models.Model):
    amr = models.ForeignKey('AmrEntry')
    human_sentence = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
