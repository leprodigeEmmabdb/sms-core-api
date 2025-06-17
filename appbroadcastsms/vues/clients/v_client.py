# appbroadcastsms/vues/Client/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from appbroadcastsms.command.cmd.smpp_client import SmppClient
from appbroadcastsms.vues.audience.sz_audience import (
    SimpleAudienceSerializer,
)
from appuser.vues.user.sz_user import UserSZ
from appbroadcastsms.models import Client, Smpp, Client
from appbroadcastsms.vues.clients.sz_client import (
    AddClientSerializer,
    UpdateClientSerializer,
    ClientSerializer,

)
from rest_framework.serializers import Serializer  # pour défaut


class ClientViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Client.objects.all().order_by('-id')

    # Sérializers selon méthode HTTP
    crud_classes = {
        "POST": AddClientSerializer,
        "PUT": UpdateClientSerializer,
        "PATCH": UpdateClientSerializer,
    }

    # Sérializers spécifiques aux actions
    actions_classes = {
        "send_single": UserSZ,
        "send_broadcast": UserSZ,
    }

    def get_serializer_class(self):
        # Retourne le serializer selon l'action ou la méthode HTTP
        if self.action in self.actions_classes:
            return self.actions_classes[self.action]
        return self.crud_classes.get(self.request.method, ClientSerializer)


