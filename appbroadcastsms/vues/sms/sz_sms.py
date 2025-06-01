from rest_framework import serializers
import re

from appbroadcastsms.models import Sms


def validate_rdc_number(value):
    """
    Valide un numéro RDC local (ex: 085255) ou international (+243...).
    """
    pattern_local = r'^0\d{8,9}$'       # Exemple: 0852551234
    pattern_intl = r'^\+243\d{8,9}$'    # Exemple: +243852551234

    if not (re.match(pattern_local, value) or re.match(pattern_intl, value)):
        raise serializers.ValidationError("Numéro invalide pour la RDC. Doit commencer par 0 ou +243.")

    return value


class SimpleSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ["id", "message"]


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = '__all__'


class AddSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ["id", "message"]


class UpdateSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ["id", "message", "is_active"]


# Serializer pour envoi à un seul numéro (pas ModelSerializer car pas directement lié à Sms)
class SendSingleSmsSerializer(serializers.Serializer):
    receiver = serializers.CharField(help_text="Numéro du destinataire", validators=[validate_rdc_number])
    message = serializers.CharField(help_text="Contenu du message", max_length=160)


# Serializer pour envoi broadcast à plusieurs numéros (idem)
class SendBroadcastMessageSerializer(serializers.Serializer):
    receivers = serializers.ListField(
        child=serializers.CharField(validators=[validate_rdc_number]),
        help_text="Liste des numéros des destinataires",
        allow_empty=False,
    )
    message = serializers.CharField(help_text="Contenu du message", max_length=160)
