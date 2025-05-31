from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localtime
from django_countries.serializers import CountryFieldMixin
from djoser.serializers import UserCreateSerializer, UserSerializer, SendEmailResetSerializer, PasswordSerializer
from rest_framework import serializers

from appuser.models import User
from appuser.user_utils import COUNTRIES_PHONE, isNumeric
from root.utils.general_utils import convertSecondsToMinSec, generate_opt_code


class SimpleUserSerializer(CountryFieldMixin, UserSerializer):
    phoneCode = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ['id', "name", "email", "phone", "postnom", "isoCode", "phone", "phoneCode"]

    def get_phoneCode(self, obj: User):
        print(type(obj.isoCode), obj.isoCode)
        return COUNTRIES_PHONE[obj.isoCode]


class DjoserCurrentUserSerializer(CountryFieldMixin, UserSerializer):
    reactions = serializers.SerializerMethodField()
    vues = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ['id', "name", "email", "phone",
                  "postnom", "isoCode", "phone",
                  "phoneCode", "reactions", "vues"]

    def get_reactions(self, obj: User):
        return 0  # TODO: add query for reactions

    def get_vues(self, obj: User):
        return 0  # TODO: add query for vues

    def get_phoneCode(self, obj: User):
        # print(type(obj.isoCode), obj.isoCode)
        return COUNTRIES_PHONE[obj.isoCode]


class DjoserUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ['id', "name", "password", "email", 'isoCode',
                  "prenom", "postnom", "phone","is_active"]

    def validate(self, data):
        data['confirm_code'] = generate_opt_code()
        data['confirm_expired_at'] = timezone.now() + timedelta(hours=1)
        phone= data['phone']
        if not isNumeric(phone):
            raise serializers.ValidationError(detail="le numéro de téléphone est incorrect")

        # TODO: SEND SMS
        return super().validate(data)


class DjoserValidateUserSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['confirm_code']

    def validate(self, data):
        confirm_code = data['confirm_code']
        q = User.objects.filter(is_active=False)

        if not q.filter(confirm_code=confirm_code).exists():
            raise serializers.ValidationError(detail="Ce code est invalide")
        user: User = q.first()

        if q.filter(confirm_expired_at__lte=timezone.now()).exists():
            q.update(can_reset=False)
            raise serializers.ValidationError(
                detail=f"Votre code a expiré. Veuillez faire une nouvelle demande de confirmation")

        if user.is_active:
            raise serializers.ValidationError(detail="Ce compte est deja validé")

        self.user = user
        return data


class DjoserResetPasswordSerializer(SendEmailResetSerializer):
    def validate(self, data):
        email = data['email']
        print("email", email)
        reset_pwd_code = generate_opt_code()
        duration = 5
        nowT = localtime(timezone.now())
        delay = nowT - timedelta(minutes=duration)
        q = User.objects.filter(email=email, is_active=True)
        if not q.exists():
            raise serializers.ValidationError(
                detail=f"Cette addresse email n'est pas reconnue ou n'est pas encore activé")
        data: User = q.first()
        reset_expired_at = data.reset_expired_at
        print(f"reset_expired_at ", reset_expired_at)
        print(f"delay ", delay)
        print("compare dates", reset_expired_at >= delay)
        if reset_expired_at >= delay:  # q.filter(reset_at__gte=delay).exists():
            c = reset_expired_at - delay
            print(f"total seconds ", c.total_seconds())
            print(f"left time ", c)
            print(f"localtime(now()) ", nowT)

            left_time = convertSecondsToMinSec(abs(c.total_seconds()))
            raise serializers.ValidationError(
                detail=f"Une demande est deja en cours. Veuillez ressayer apres {left_time}")

        expired_at = timezone.now() + timedelta(minutes=duration)
        User.objects.filter(email=email). \
            update(reset_pwd_code=reset_pwd_code, reset_at=timezone.now(),
                   reset_expired_at=expired_at, can_reset=True)

        return super().validate(data)


class DjoserResendMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        email = data.pop('email')
        print("email", email)
        new_confirm_code = generate_opt_code()
        duration = 5
        delay = timezone.now() - timedelta(minutes=duration)
        q: User = self.instance

        confirm_expired_at = q.confirm_expired_at
        if confirm_expired_at >= delay:
            c = confirm_expired_at - timezone.now()
            left_time = convertSecondsToMinSec(c.seconds)
            raise serializers.ValidationError(
                detail=f"Une demande est deja en cours. Veuillez ressayer apres {left_time}")

        expired_at = timezone.now() + timedelta(minutes=duration)
        data['confirm_expired_at'] = expired_at
        data['confirm_code'] = new_confirm_code

        return super().validate(data)


class DjoserValidatePwdResetSerializer(PasswordSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email", "new_password"]

    def validate(self, data):
        email = data['email']
        q = User.objects.filter(email=email, is_active=True, can_reset=True)

        if not q.exists():
            raise serializers.ValidationError(
                detail="Ce compte n'existe ou n'a pas initié une demande de reinitialisation")

        user: User = q.first()
        if not user.reset_code_valid:
            raise serializers.ValidationError(detail="Veuillez confirmer le code de validation au prealable")

        q.update(can_reset=False)
        print("q update", q.query, flush=True)
        self.user = user
        return data


class ConfirmResetCodeSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "reset_pwd_code"]

    def validate(self, data):
        user: User = self.instance
        if not user.can_reset:
            raise serializers.ValidationError(detail="Veuillez faire une nouvelle demande "
                                                     "de reinitialisation")

        if user.reset_expired_at <= timezone.now():
            raise serializers.ValidationError(
                detail=f"Votre code a expiré. Veuillez faire une nouvelle demande de réinitialisation")

        data['reset_code_valid'] = True
        data['reset_confirmed_at'] = timezone.now()
        return data


class EmptySZ(serializers.Serializer):
    class Meta:
        fields = []


class ChangeUsernameSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]


class UpdateUserSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "prenom"]

    def validate(self, data):
        if data.get('email'):
            q = User.objects.filter(~Q(id=self.instance.id), email__iexact=data['email'])
            if q.exists():
                raise serializers.ValidationError(detail=f"Cette adresse email est "
                                                         f"deja utilisé")

        return super().validate(data)


class UserSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude = ["password"]
        fields = ['id', "is_superuser", "name",
                  "prenom", "postnom", "is_active", "is_staff", "email"]
