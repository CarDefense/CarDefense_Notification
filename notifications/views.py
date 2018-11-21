from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import MessageTooBigError
from exponent_server_sdk import MessageRateExceededError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from rest_framework.viewsets import ModelViewSet
from notifications.models import Notifications, EmergencyNotifications, NotificationsImage
from .serializers import NotificationsSerializer, EmergencyNotificationsSerializer, NotificationsImageSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, filters
import requests


URL = 'http://cardefense3.eastus.cloudapp.azure.com'


class NotificationsImageViewSet(ModelViewSet):
    queryset = NotificationsImage.objects.all()
    serializer_class = NotificationsImageSerializer


class NotificationsViewSet(ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id',)

    def get_queryset(self):
        id_token = self.request.query_params.get("token")
        return Notifications.objects.filter(id_token=id_token)


class EmergencyNotificationsViewSet(ModelViewSet):
    queryset = EmergencyNotifications.objects.all()
    serializer_class = EmergencyNotificationsSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id',)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_push_message(request):

    plate = request.data['plate']
    sender_id = request.data["sender_id"]
    title = request.data["title"]
    message = request.data["message"]
    image = request.data["image"]

    messageArray = []

    try:
        task = {"plate": plate}
        idTokenArray = requests.post(URL + ':8003/get_id_token/', json=task)
    except (ConnectionError, HTTPError):
        return Response("Could not to connect to cars", status.HTTP_503_SERVICE_UNAVAILABLE)

    try:
        if (idTokenArray.json()):
            task = {"token_array": idTokenArray.json()}
            notificationTokenArray = requests.post(URL + ':8005/get_notification_token/', json=task)

        else:
            return Response("Placa não cadastrada.")
    except (ConnectionError, HTTPError):
        return Response("Could not to connect to profile", status.HTTP_503_SERVICE_UNAVAILABLE)

    try:
        task = {"sender_id": sender_id}
        senderToken = requests.post(URL + ':8005/get_token/', json=task)
    except (ConnectionError, HTTPError):
        return Response("Could not to connect to profile", status.HTTP_503_SERVICE_UNAVAILABLE)

    for token in notificationTokenArray.json():
        if(token != senderToken.json() and 'ExponentPushToken' in token):
            messageArray.append(PushMessage(to=token, title=title, body=message))

    try:
        responseArray = PushClient().publish_multiple(messageArray)
    except (ConnectionError, HTTPError):
        return Response("Could not connect to ExpoSever", status.HTTP_502_BAD_GATEWAY)
    except (PushServerError):
        return Response("Push Server Error", status.HTTP_502_BAD_GATEWAY)

    i = 0
    for response in responseArray:
        try:
            response.validate_response()
        except DeviceNotRegisteredError:
            pass
        except MessageTooBigError:
            return Response("Message too big", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        except MessageRateExceededError:
            i = i + 1

    j = len(responseArray)
    if i > (j/2):
        return Response("Error", status.HTTP_503_SERVICE_UNAVAILABLE)

    for token in idTokenArray.json():
        if(token != sender_id):
            Notifications.objects.create(id_token=token, title=title, message=message, image=image)

    return Response("Notificação enviada!", status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_emergency_push_message(request):

    sender_id = request.data["sender_id"]
    title = request.data["title"]
    message = request.data["message"]
    image = request.data["image"]

    messageArray = []
    try:
        notificationTokenArray = requests.get(URL + ':8005/notification_token/')
    except (ConnectionError, HTTPError):
        return Response("Could not connect to profile", status.HTTP_502_BAD_GATEWAY)

    try:
        task = {"sender_id": sender_id}
        senderToken = requests.post(URL + ':8005/get_token/', json=task)
    except (ConnectionError, HTTPError):
        return Response("Could not to connect to profile", status.HTTP_503_SERVICE_UNAVAILABLE)

    for token in notificationTokenArray.json():
        if(token != senderToken.json() and 'ExponentPushToken' in token):
            messageArray.append(PushMessage(to=token, title=title, body=message))

    try:
        responseArray = PushClient().publish_multiple(messageArray)
    except (ConnectionError, HTTPError):
        return Response("Could not connect to ExpoSever", status.HTTP_502_BAD_GATEWAY)
    except (PushServerError):
        return Response("Push Server Error", status.HTTP_502_BAD_GATEWAY)

    i = 0
    for response in responseArray:
        try:
            response.validate_response()
        except DeviceNotRegisteredError:
            pass
        except MessageTooBigError:
            return Response("Message too big", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        except MessageRateExceededError:
            i = i + 1

    j = len(responseArray)
    if i > (j/2):
        return Response("Error", status.HTTP_503_SERVICE_UNAVAILABLE)

    EmergencyNotifications.objects.create(title=title, message=message, image=image)

    return Response("Alerta enviado!",status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_push_message_admin(request):

    id = request.data['id']
    token = request.data['token']
    title = request.data['title']
    message = request.data['message']
    image = request.data['image']

    try:
        response = PushClient().publish(
            PushMessage(to=token, title=title, body=message))
    except PushServerError:
        return Response("Push Server Error", status.HTTP_502_BAD_GATEWAY)
    except (ConnectionError, HTTPError):
        return Response("Could not connect to ExpoSever", status.HTTP_502_BAD_GATEWAY)
    except (ValueError):
        return Response("Recipient not registered", status.HTTP_404_NOT_FOUND)
    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        return Response("Recipient not registered", status.HTTP_404_NOT_FOUND)
    except MessageTooBigError:
        return Response("Message too big", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
    except MessageRateExceededError:
        return Response("Error", status.HTTP_503_SERVICE_UNAVAILABLE)
    except PushResponseError:
        return Response("Recipient not registered", status.HTTP_404_NOT_FOUND)

    Notifications.objects.create(id_token=id, title=title, message=message, image=image)

    return Response("Mensagem enviada!",status.HTTP_200_OK)
