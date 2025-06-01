from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from appbroadcastsms.models import Smpp
from appbroadcastsms.vues.smpp.sz_smpp import (
    AddSmppSerializer, SmppSerializer, UpdateSmppSerializer,
    SendMessageToOneClientSerializer, SendMessageToMultipleClientsSerializer
)
from appbroadcastsms.command.cmd.smpp_client import send_sms


class SmppViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Smpp.objects.all()

    crud_classes = {
        "POST": AddSmppSerializer,
        "PUT": UpdateSmppSerializer,
        "PATCH": UpdateSmppSerializer,
    }

    actions_classes = {
        "send_single": SendMessageToOneClientSerializer,
        "send_broadcast": SendMessageToMultipleClientsSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.actions_classes:
            return self.actions_classes[self.action]
        return self.crud_classes.get(self.request.method, SmppSerializer)

    @action(detail=False, methods=['POST'], name="Send SMPP to single receiver")
    def send_single(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = serializer.validated_data['client_id']
        sms = serializer.validated_data['message_id']

        try:
            send_sms(client.numero, sms.message)  # adapte le champ au modèle Client/Sms

            smpp_obj = Smpp.objects.create(message=sms, client=client)

        except Exception as e:
            return Response({"error": f"Sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "Message sent successfully", "smpp_id": smpp_obj.id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], name="Send SMPP to multiple receivers")
    def send_broadcast(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clients = serializer.validated_data['client_ids']
        sms = serializer.validated_data['message_id']

        numeros = [client.numero for client in clients]

        try:
            send_sms(numeros, sms.message)

            envois = [Smpp(message=sms, client=client) for client in clients]
            Smpp.objects.bulk_create(envois)

        except Exception as e:
            return Response({"error": f"Sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "All messages sent successfully"}, status=status.HTTP_200_OK)
