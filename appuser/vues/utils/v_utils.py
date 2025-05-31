from django.core.mail import send_mail
from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from app_user.models import Agent, User
from app_user.vues.agent.sz_agent import AddAgentSZ, UpdateAgentSZ, AgentSZ
from app_user.vues.user.user_sz import EmptySZ, ChangeUsernameSZ, DjoserCurrentUserSerializer
from app_user.vues.utils.sz_send_email import SendEmailSZ


# @method_decorator(cache_page(0 * 2), name='dispatch')
class UtilitairesViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.filter(id=0)

    sz_classes = {"POST": EmptySZ}
    sz_action_classes = {
        'sendEmail': SendEmailSZ,
    }
    default_sz = DjoserCurrentUserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        print('self.action', self.action, flush=True)
        action = self.sz_action_classes.get(self.action)
        if action:
            return action
        return self.sz_classes.get(self.request.method, self.default_sz)

    @action(detail=False, methods=['POST'], name="Send email")
    def sendEmail(self, request: HttpRequest, **kwargs):
        # if request.method in ["POST"]:
        sz = SendEmailSZ(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(sz.data)
    # return Response(SendEmailSZ().data)
