from django.db import models


class Notification(models.Model):
    token = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class NotificationEmergency(models.Model):
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=150)

    def __str__(self):
        return self.title
