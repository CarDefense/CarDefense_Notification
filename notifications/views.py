from rest_framework.viewsets import ModelViewSet
from notifications.models import Notification, NotificationEmergency
from .serializers import NotificationSerializer, NotificationEmergencySerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationEmergencyViewSet(ModelViewSet):
    queryset = NotificationEmergency.objects.all()
    serializer_class = NotificationEmergencySerializer
