from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class AmrEntry(models.Model):
    sentence = models.CharField(max_length=1000)
    amr = models.CharField(max_length=5000)
    reference_number = models.IntegerField()


class Generation(models.Model):
    amr = models.ForeignKey('AmrEntry')
    human_sentence = models.CharField(max_length=1000)
