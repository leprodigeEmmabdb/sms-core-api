# appbroadcastsms/vues/sms/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from appbroadcastsms.command.cmd.smpp_client import smpp_client  # import du singleton

from appbroadcastsms.models import Sms, Smpp
from appbroadcastsms.vues.sms.sz_sms import (
    AddSmsSerializer,
    UpdateSmsSerializer,
    SmsSerializer,
)
from appuser.vues.user.sz_user import EmptySZ


class SmsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Sms.objects.all()
    
    crud_classes = {
        "POST": AddSmsSerializer,
        "PUT": UpdateSmsSerializer,
        "PATCH": UpdateSmsSerializer,
    }
    
    actions_classes = {
        "send_single": EmptySZ,
        "send_broadcast": EmptySZ,
    }

    def get_serializer_class(self):
        if self.action in self.actions_classes:
            return self.actions_classes[self.action]
        return self.crud_classes.get(self.request.method, SmsSerializer)
    
    @action(detail=False, methods=['POST'], name="Send SMS to single receiver")
    def send_single(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = serializer.validated_data['client_id']
        sms = serializer.validated_data['message_id']

        try:
            smpp_client.send_sms(client.numero, sms.message)

            smpp_obj = Smpp.objects.create(message=sms, client=client)

        except Exception as e:
            return Response({"error": f"Sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "Message sent successfully", "smpp_id": smpp_obj.id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], name="Send SMS to multiple receivers")
    def send_broadcast(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clients = serializer.validated_data['client_ids']
        sms = serializer.validated_data['message_id']

        numeros = [client.numero for client in clients]

        try:
            smpp_client.send_sms(numeros, sms.message)

            envois = [Smpp(message=sms, client=client) for client in clients]
            Smpp.objects.bulk_create(envois)

        except Exception as e:
            return Response({"error": f"Sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "All messages sent successfully"}, status=status.HTTP_200_OK)
