from django.db import models


class Notifications(models.Model):
    token = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)


class EmergencyNotifications(models.Model):
    title = models.CharField(max_length=10)
    message = models.CharField(max_length=50)
