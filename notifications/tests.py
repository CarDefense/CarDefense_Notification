from rest_framework import status
from .models import Notifications
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
import json


class NotificationsTests(APITestCase):
    def test_create_notification(self):
        url = 'http://68.183.28.199:8002/notifications/'
        data = {'token': 'test token', 'title': 'test title', 'message': 'test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notifications.objects.count(), 1)
        self.assertEqual(Notifications.objects.get().token, 'test token')

    def testing_post(factory):
        "Testing post requests"
        factory = APIRequestFactory()
        factory.post('/send_push_message/', json.dumps(
            {'plate': 'xxxxxx', 'token': 'test token', 'title': 'test title', 'message': 'test message'}),
            content_type='application/json')

    def testing_get(client):
        client = APIClient()
        client.get('http://68.183.28.199:8002/emergencynotifications/')
