"""api_notification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from notifications.views import NotificationsViewSet, EmergencyNotificationsViewSet
from notifications.views import send_push_message, send_emergency_push_message


router = routers.SimpleRouter()
router.register(r'notifications', NotificationsViewSet)
router.register(r'emergencynotifications', EmergencyNotificationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^send_push_message/$', send_push_message),
    url(r'^send_emergency_push_message/$', send_emergency_push_message)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
