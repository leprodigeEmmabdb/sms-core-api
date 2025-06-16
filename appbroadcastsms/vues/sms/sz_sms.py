# appbroadcastsms/vues/sms/sz_sms.py

import re
from rest_framework import serializers
from appbroadcastsms.models import Sms


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
        exclude = ['is_active']

class UpdateSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ['id', 'message', 'is_active']

# Serializer pour un seul destinataire
class SendSingleSmsSerializer(serializers.Serializer):
    numero = serializers.CharField()
    message = serializers.CharField()

# Serializer pour plusieurs destinataires
class SendBroadcastSmsSerializer(serializers.Serializer):
    phone_numbers = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()

