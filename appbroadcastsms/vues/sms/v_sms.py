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
            "Send SMS to single receiver": EmptySZ,
            "Send SMS to multiple receivers": EmptySZ,
        }

    def get_serializer_class(self):
        action_sz= self.actions_classes.get(self.action)
        if action_sz:
            return action_sz
        
        return self.crud_classes.get(self.request.method, SmsSerializer)
    
