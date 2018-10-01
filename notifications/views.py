from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError
from exponent_server_sdk import PushResponseError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from rest_framework.viewsets import ModelViewSet
from notifications.models import Notifications, EmergencyNotifications
from .serializers import NotificationsSerializer, EmergencyNotificationsSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from rest_framework import status
from self import self
import rollbar
import requests


class NotificationsViewSet(ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        token = self.request.query_params.get("token")
        return Notifications.objects.filter(token=token)


class EmergencyNotificationsViewSet(ModelViewSet):
    queryset = EmergencyNotifications.objects.all()
    serializer_class = EmergencyNotificationsSerializer


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_push_message(request):

    plate = request.data['plate']

    task = {"plate": plate}
    token_data = requests.post('http://68.183.28.199:8005/get_notification_token/', json=task)
    token = token_data.json()

    title = request.data['title']
    message = request.data['message']

    try:
        response = PushClient().publish(
            PushMessage(to=token, title=title, body=message))
    except PushServerError as exc:
        rollbar.report_exc_info(
            extra_data={'token': token, 'title': title, 'message': message})
        raise
    except (ConnectionError, HTTPError) as exc:
        rollbar.report_exc_info(
            extra_data={'token': token, 'title': title, 'message': message})
        raise self.retry(exc=exc)
    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        rollbar.report_exc_info(
            extra_data={'token': token, 'title': title, 'message': message,
                        'push_response': exc.push_response._asdict(), })
        raise self.retry(exc=exc)

    task = {"token": token, "title": title, "message": message}
    resp = requests.post('http://68.183.28.199:8002/notifications/', json=task)
    return Response(resp)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_emergency_push_message(request):

    # sender_id = request.data["sender_id"]
    title = request.data["title"]
    message = request.data["message"]

    messagesArray = []
    tokensArray = requests.get('http://68.183.28.199:8005/notification_token/')

    for token in tokensArray.json():
        messagesArray.append(PushMessage(to=token, title=title,
                                         body=message))

    PushClient().publish_multiple(messagesArray)

    task = {"title": title, "message": message}
    resp = requests.post('http://68.183.28.199:8002/emergencynotifications/', json=task)

    # if resp.status_code != 201:
    #    raise ApiError('POST /tasks/ {}'.format(resp.status_code))
    #    print('Created task. ID: {}'.format(resp.json()["id"]))

    return Response(resp)

    #    elif request.method == 'POST':
    #    serializer = SnippetSerializer(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # adicionar exceção de PushServerError
    # adicionar exceção de ConnectionError
    # adicionar exceção de HTTPError
    # adicionar exceção de DeviceNotRegisteredError
    # adicionar exceção de PushResponseError
    # adicionar retorno status.HTTP_200_OK
