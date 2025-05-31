from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from appuser.models import User
from appuser.vues.user.sz_user import UpdateUserSZ, UserSZ, EmptySZ, ConfirmResetCodeSZ, DjoserResendMailSerializer
from root.utils.emails_utils import TemplateEmail


# @method_decorator(cache_page(0 * 2), name='dispatch')
class UserPublicViewSet(ModelViewSet):
    http_method_names = ["post", "put", "patch"]

    sz_classes = {'POST': EmptySZ, }
    sz_action_classes = {"confirm_reset_pwd": ConfirmResetCodeSZ, "resent_activation": DjoserResendMailSerializer}
    default_sz = UserSZ
    queryset = User.objects.order_by('-id')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_fields = []
    ordering_fields = []
    permission_classes = []

    def get_serializer_class(self):
        action = self.sz_action_classes.get(self.action)
        if action: return action
        print("self.request.method", self.request.method)
        return self.sz_classes.get(self.request.method, self.default_sz)

    @action(detail=False, methods=['POST'], name="confirm pwd code")
    def confirm_reset_pwd(self, request: HttpRequest, **kwargs):
        data = request.data
        reset_pwd_code = data['reset_pwd_code']
        q = User.objects.filter(reset_pwd_code=reset_pwd_code)
        if not q.exists():
            raise serializers.ValidationError(detail="Ce code est invalide")

        sz = ConfirmResetCodeSZ(q.first(), data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(sz.data)

    @action(detail=False, methods=['PUT'], name="resend activation")
    def resent_activation(self, request: HttpRequest, **kwargs):
        data = request.data
        q = User.objects.filter(email=data['email'])
        if not q.exists():
            raise serializers.ValidationError(detail=f"Cette addresse email n'est pas reconnue")

        sz = DjoserResendMailSerializer(q.first(), data=data)
        sz.is_valid(raise_exception=True)
        sz.save()
        instance: User = sz.instance

        template = TemplateEmail(
            to=[instance.email],
            subject=f"Code de confirmation PesaSango",
            template="resent_activation_mail",
            context={"site_name": "PesaSango", "confirm_code": instance.confirm_code},
        )
        template.send()
        return Response(sz.data)
