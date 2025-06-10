# appbroadcastsms/vues/sms/sz_sms.py

import re
from rest_framework import serializers
from appbroadcastsms.models import Sms

def validate_rdc_number(value):
    """
    Valide un numéro RDC local (ex: 0852551234) ou international (+243852551234).
    """
    pattern_local = r'^0\d{8,9}$'
    pattern_intl = r'^\+243\d{8,9}$'

    if not (re.match(pattern_local, value) or re.match(pattern_intl, value)):
        raise serializers.ValidationError("Numéro invalide pour la RDC. Format accepté: 0XXXXXXXXX ou +243XXXXXXXXX.")
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
        fields = ['message']

class UpdateSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ['id', 'message', 'is_active']

class SendSingleSmsSerializer(serializers.Serializer):
    receiver = serializers.CharField(validators=[validate_rdc_number])
    message = serializers.CharField(max_length=160)

class SendBroadcastMessageSerializer(serializers.Serializer):
    receivers = serializers.ListField(
        child=serializers.CharField(validators=[validate_rdc_number]),
        allow_empty=False
    )
    message = serializers.CharField(max_length=160)
    
class SendFileSmsSerializer(serializers.Serializer):
    file = serializers.FileField()
    message = serializers.CharField(max_length=160)

    def validate_file(self, value):
        if not value.name.endswith(('.xlsx', '.xls', '.csv')):
            raise serializers.ValidationError("Format de fichier non supporté. Utilisez un fichier .xlsx, .xls ou .csv.")
        return value