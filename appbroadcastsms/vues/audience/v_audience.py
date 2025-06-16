# appbroadcastAudience/vues/audience/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from appbroadcastsms.command.cmd.smpp_client import SmppClient
from appbroadcastsms.models import Smpp, Client  # Ajout de Client
from appbroadcastsms.vues.audience.sz_audience import (
    # UpdateAudienceSerializer,
    AudienceSerializer,     # idem
)
from appuser.vues.user.sz_user import EmptySZ


class AudienceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    queryset = Smpp.objects.all().order_by('id')
    serializer_class = AudienceSerializer