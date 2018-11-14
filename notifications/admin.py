from django.contrib import admin
from .models import Notifications, EmergencyNotifications, NotificationsImage


admin.site.register(Notifications)
admin.site.register(EmergencyNotifications)
admin.site.register(NotificationsImage)
