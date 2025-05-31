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
class UserViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "put"]

    sz_classes = {'POST': EmptySZ, "PUT": UpdateUserSZ,
                  "PATCH": UpdateUserSZ}
    sz_action_classes = {"confirm_reset_pwd": ConfirmResetCodeSZ,
                      }
    default_sz = UserSZ
    queryset = User.objects \
        .order_by('-id')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username']
    filterset_fields = ['is_active']
    ordering_fields = ['id', "username"]
    permission_classes = [IsAuthenticated]

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


