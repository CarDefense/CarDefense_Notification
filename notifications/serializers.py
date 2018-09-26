from rest_framework.serializers import ModelSerializer
from .models import Notification, NotificationEmergency, APIUser


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationEmergencySerializer(ModelSerializer):
    class Meta:
        model = NotificationEmergency
        fields = '__all__'


class APIUserSerializer(ModelSerializer):
    class Meta:
        model = APIUser
        fields = '__all__'
