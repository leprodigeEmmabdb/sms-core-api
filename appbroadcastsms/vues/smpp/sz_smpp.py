from rest_framework import serializers
from appbroadcastsms.command.cmd.smpp_client import send_sms
from appbroadcastsms.models import Client, Smpp, Sms
from appbroadcastsms.vues.client.sz_client import SimpleClientSerializer
from appbroadcastsms.vues.sms.sz_sms import SimpleSmsSerializer


class SmppSerializer(serializers.ModelSerializer):
    client = SimpleClientSerializer(read_only=True)
    message = SimpleSmsSerializer(read_only=True)

    class Meta:
        model = Smpp
        fields = '__all__'


class AddSmppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smpp
        fields = ["id", "client", "message"]


class UpdateSmppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smpp
        fields = ["id", "client", "message"]


class SendMessageToOneClientSerializer(serializers.Serializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Sms.objects.all())
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    def create(self, validated_data):
        client_obj = validated_data['client_id']
        message_obj = validated_data['message_id']

        # Envoi du SMS
        send_sms(client_obj.numero, message_obj.message)

        # Création en base
        envoi = Smpp.objects.create(
            message=message_obj,
            client=client_obj
        )
        return envoi


class SendMessageToMultipleClientsSerializer(serializers.Serializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Sms.objects.all())
    client_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Client.objects.all())

    def create(self, validated_data):
        message_obj = validated_data['message_id']
        clients = validated_data['client_ids']

        numeros = [client.numero for client in clients]

        # Envoi SMS broadcast
        send_sms(numeros, message_obj.message)

        # Enregistrements en base
        envois = [Smpp(message=message_obj, client=client) for client in clients]
        Smpp.objects.bulk_create(envois)

        return envois
