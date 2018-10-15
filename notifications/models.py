from django.db import models


class Notifications(models.Model):
    token = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)


class EmergencyNotifications(models.Model):
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=50)
    image = models.CharField(max_length=70)


class NotificationsImage(models.Model):
    image = models.ImageField(upload_to='images')
