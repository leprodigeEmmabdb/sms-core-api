from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from appbroadcastsms.models import Client
from appbroadcastsms.vues.client.sz_client import AddClientSerializer, ClientSerializer, UpdateClientSerializer
from appuser.vues.user.sz_user import EmptySZ

# ViewSets define the view behavior.
class ClientViewSet(viewsets.ModelViewSet):
    
    http_method_names=['get',"post","put","patch"]
    queryset = Client.objects.all()

    crud_classes={"POST": AddClientSerializer, 
                  "PUT":UpdateClientSerializer, 
                  "PATCH": UpdateClientSerializer}

    actions_classes = {
            "Send Client to single receiver": EmptySZ,
            "Send Client to multiple receivers": EmptySZ,
        }

    def get_serializer_class(self):
        action_sz= self.actions_classes.get(self.action)
        if action_sz:
            return action_sz
        
        return self.crud_classes.get(self.request.method, ClientSerializer)
    
