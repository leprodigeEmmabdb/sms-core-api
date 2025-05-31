from rest_framework import serializers

from appbroadcastsms.models import Sms


# Serializers define the API representation.

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
        fields = ["id", "message","is_active"]

# Serializer pour envoi à un seul numéro
class SendSingleSmsSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(help_text="Numéro du destinataire")
    message = serializers.CharField(help_text="Contenu du message")
    

# Serializer pour envoi broadcast à plusieurs numéros
class SendBroadcastMessageSerializer(serializers.ModelSerializer):
    receivers = serializers.ListField(
        child=serializers.CharField(),
        help_text="Liste des numéros des destinataires"
    )
    message = serializers.CharField(help_text="Contenu du message")