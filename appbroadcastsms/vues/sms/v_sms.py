from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from appbroadcastsms.models import Sms
from appbroadcastsms.vues.sms.sz_sms import AddSmsSerializer, SendBroadcastMessageSerializer, SendBroadcastMessageSerializer, SendSingleSmsSerializer, SmsSerializer, UpdateSmsSerializer
from appuser.vues.user.sz_user import EmptySZ

# ViewSets define the view behavior.
class SmsViewSet(viewsets.ModelViewSet):
    http_method_names=['get',"post","put","patch"]
    queryset = Sms.objects.all()

    crud_classes={"POST": AddSmsSerializer, 
                  "PUT":UpdateSmsSerializer, 
                  "PATCH": UpdateSmsSerializer}

    actions_classes = {
            "Send SMS to single receiver": SendSingleSmsSerializer,
            "Send SMS to multiple receivers": SendBroadcastMessageSerializer,
        }

    def get_serializer_class(self):
        action_sz= self.actions_classes.get(self.action)
        if action_sz:
            return action_sz
        
        return self.crud_classes.get(self.request.method, SmsSerializer)
    
    @action(detail=False, methods=['POST'], name="Send SMS to single receiver")
    def send_single(self, request):
        serializer = SendSingleSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data['receiver']
        message = serializer.validated_data['message']

        try:
            smpp_client.send_sms(receiver, message)
        except Exception as e:
            return Response({"error": f"Sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "Message sent successfully"}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'], name="Send SMS to multiple receivers")
    def send_broadcast(self, request):
        serializer = SendBroadcastMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receivers = serializer.validated_data['receivers']
        message = serializer.validated_data['message']

        errors = []
        for receiver in receivers:
            try:
                smpp_client.send_sms(receiver, message)
            except Exception as e:
                errors.append({"receiver": receiver, "error": str(e)})

        if errors:
            return Response({"status": "Partial failure", "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
        else:
            return Response({"status": "All messages sent successfully"}, status=status.HTTP_200_OK)