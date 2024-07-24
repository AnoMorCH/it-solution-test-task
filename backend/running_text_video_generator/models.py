from django.db import models


class TextLog(models.Model):
    text = models.TextField()
