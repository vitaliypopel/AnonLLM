from django.db import models


class Message(models.Model):
    # Model saving question from user and answer from LLM
    # Attribute session_id is a current csrf token (which always the same) and hashed using md5

    session_id = models.CharField(max_length=32)
    question = models.CharField(max_length=20000)
    answer = models.CharField(max_length=100000)
