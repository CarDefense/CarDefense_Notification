from django.db import models


class Notifications(models.Model):
    id_token = models.BigIntegerField()
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)
    image = models.CharField(null=True, blank=True, max_length=250)


class EmergencyNotifications(models.Model):
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)
    image = models.CharField(null=True, blank=True, max_length=250)


class NotificationsImage(models.Model):
    image = models.ImageField(null=True, blank=True)
