from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError
'''from exponent_server_sdk import PushResponseError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError'''
from rest_framework.viewsets import ModelViewSet
from notifications.models import Notification, NotificationEmergency, APIUser
from .serializers import NotificationSerializer, NotificationEmergencySerializer, APIUserSerializer
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


class APIUserViewSet(ModelViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_push_message(request):
    token = request.data['token']
    title = request.data['title']
    message = request.data['message']

    try:
        response = PushClient().publish(
            PushMessage(to=token, title=title, body=message))
    except PushServerError as exc:
        rollbar.report_exc_info(
            extra_data={'token': token, 'title': title, 'message': message})
        raise
#    except (ConnectionError, HTTPError) as exc:
#        rollbar.report_exc_info(
#            extra_data={'token': token, 'title': title, 'message': message})
#        raise self.retry(exc=exc)
    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
#    except PushResponseError as exc:
#        rollbar.report_exc_info(
#            extra_data={'token': token, 'title': title, 'message': message,
#                        'push_response': exc.push_response._asdict(), })
#        raise self.retry(exc=exc)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def send_emergency_push_message(request):

    title = request.data['title']
    message = request.data['message']

    messagesArray = []
    for e in APIUser.objects.all():
        messagesArray.append(PushMessage(to=e.deviceId, title=title, body=message))

    response = PushClient().publish_multiple(messagesArray)
    return Response(response)

#    token.append(e.deviceId
#        i = i + 1
#        tst = []
#    for tk in token:
#        return Response(token)
#    try:
#        response =
#    PushClient().publish(PushMessage(to=token, title=title, body=message))
#    except PushServerError as exc:
#        rollbar.report_exc_info(
#            extra_data={'token': token, 'title': title, 'message': message,
#                        'errors': exc.errors,
#                        'response_data': exc.response_data, })
#        raise
#    except (ConnectionError, HTTPError) as exc:
#        rollbar.report_exc_info(
#            extra_data={'token': token, 'title': title, 'message': message})
#        raise self.retry(exc=exc)
#        try:
#            response.validate_response()
#        except DeviceNotRegisteredError:
#            from notifications.models import PushToken
#            PushToken.objects.filter(token=token).update(active=False)
#        except PushResponseError as exc:
#            rollbar.report_exc_info(
#               extra_data={'token': token, 'title': title, 'message': message,
#                            'push_response': exc.push_response._asdict(), })
#            raise self.retry(exc=exc)
#            return Response(status=status.HTTP_200_OK)
