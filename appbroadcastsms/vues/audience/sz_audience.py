# appbroadcastAudience/vues/Audience/sz_Audience.py

import re
from rest_framework import serializers
from appbroadcastsms.models import Smpp
from appbroadcastsms.vues.sms.sz_sms import SimpleSmsSerializer


class SimpleAudienceSerializer(serializers.ModelSerializer):
    message=SimpleSmsSerializer()
    class Meta:
        model = Smpp
        fields = ["id", "message"]

class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smpp
        fields = '__all__'


# class UpdateAudienceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Audience
#         fields = ['id', 'message', 'is_active']

