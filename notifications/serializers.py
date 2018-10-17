from rest_framework import serializers
from .models import Notifications, EmergencyNotifications, NotificationsImage


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class EmergencyNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyNotifications
        fields = '__all__'


class NotificationsImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = NotificationsImage
        fields = '__all__'
