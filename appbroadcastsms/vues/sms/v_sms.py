# appbroadcastsms/vues/sms/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from appbroadcastsms.command.cmd.smpp_client import SmppClient
from appbroadcastsms.models import Sms, Smpp, Client  # Ajout de Client
from appbroadcastsms.vues.sms.sz_sms import (
    AddSmsSerializer,
    UpdateSmsSerializer,
    SmsSerializer,
    SendSingleSmsSerializer,       # nouveau serializer adapté
    SendBroadcastSmsSerializer     # idem
)
from rest_framework.serializers import Serializer  # pour défaut


class SmsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Sms.objects.all().order_by('-id')

    crud_classes = {
        "POST": AddSmsSerializer,
        "PUT": UpdateSmsSerializer,
        "PATCH": UpdateSmsSerializer,
    }

    actions_classes = {
        "send_single": SendSingleSmsSerializer,
        "send_broadcast": SendBroadcastSmsSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.actions_classes:
            return self.actions_classes[self.action]
        return self.crud_classes.get(self.request.method, SmsSerializer)

    def get_smpp_client(self):
        # Méthode pour récupérer le client SMPP injecté ou global
        if not hasattr(self, '_smpp_client'):
            self._smpp_client = SmppClient()
        return self._smpp_client

    @action(detail=False, methods=['POST'], name="Send SMS to single receiver")
    def send_single(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        numero = serializer.validated_data['numero']
        message = serializer.validated_data['message']

        try:
            client, created = Client.objects.get_or_create(numero=numero)
            sms = Sms.objects.create(message=message)

            smpp = self.get_smpp_client()
            pdu = smpp.send_sms(client.numero, sms.message)


            # if pdu is None:
            #     raise ValueError("Aucune réponse du SMSC, pdu est None")

            # safe access now
            smpp_obj = Smpp.objects.create(
                message=sms,
                client=client,
                code_retour=str(getattr(pdu, 'status', 'NO_STATUS')),
                message_id_smsc=getattr(pdu, 'message_id', None)
            )
            return Response({
                "status": "Message sent successfully",
                "smpp_id": smpp_obj.id,
                "client_created": created
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Sending failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], name="Send SMS to multiple receivers")
    def send_broadcast(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_numbers = serializer.validated_data['phone_numbers']
        message = serializer.validated_data['message']

        try:
            sms = Sms.objects.create(message=message)
            clients, new_clients = [], []

            for number in phone_numbers:
                client, created = Client.objects.get_or_create(numero=number)
                clients.append(client)
                if created:
                    new_clients.append(number)

            smpp = self.get_smpp_client()
            pdus = smpp.send_sms([c.numero for c in clients], sms.message)

            envois = []
            for client, pdu in zip(clients, pdus):
                envois.append(Smpp(
                    message=sms,
                    client=client,
                    code_retour=str(pdu.status),
                    message_id_smsc=getattr(pdu, 'message_id', None)
                ))

            Smpp.objects.bulk_create(envois)

            return Response({
                "status": "All messages sent successfully",
                "sent_count": len(envois),
                "new_clients": new_clients
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Sending failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
