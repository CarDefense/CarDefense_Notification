from rest_framework.serializers import ModelSerializer
from .models import Notifications, EmergencyNotifications


class NotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class EmergencyNotificationsSerializer(ModelSerializer):
    class Meta:
        model = EmergencyNotifications
        fields = '__all__'
