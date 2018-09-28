from rest_framework.serializers import ModelSerializer
from .models import Notification, EmergencyNotifications


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class EmergencyNotificationsSerializer(ModelSerializer):
    class Meta:
        model = EmergencyNotifications
        fields = '__all__'
