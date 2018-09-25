from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from rest_framework.viewsets import ModelViewSet
from notifications.models import Notification, NotificationEmergency
from .serializers import NotificationSerializer, NotificationEmergencySerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import rollbar


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationEmergencyViewSet(ModelViewSet):
    queryset = NotificationEmergency.objects.all()
    serializer_class = NotificationEmergencySerializer


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_push_message(request):
    token =  request.data['token']
    title =  request.data['title']
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
            extra_data={'token': token, 'title': title, 'message': message,'push_response': exc.push_response._asdict(),})
        raise self.retry(exc=exc)
    return Response(status=status.HTTP_200_OK)
