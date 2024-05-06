from django.db import models


class Message(models.Model):
    session_id = models.CharField(max_length=32)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000000)
