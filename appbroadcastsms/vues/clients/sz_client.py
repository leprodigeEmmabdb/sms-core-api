# appbroadcastClient/vues/Client/sz_Client.py

import re
from rest_framework import serializers
from appbroadcastsms.models import Client


def validate_numero_format(value):
    """
    Vérifie que le numéro commence par  243 ou 8 et contient uniquement des chiffres ensuite.
    """
    if not re.match(r'^(?:\+243|243|8)\d+$', value):
        raise serializers.ValidationError("Le numéro doit commencer par 243 ou 8 et contenir uniquement des chiffres.")
    return value


class SimpleClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "numero"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class AddClientSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(validators=[validate_numero_format])

    class Meta:
        model = Client
        exclude = ['is_active']


class UpdateClientSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(validators=[validate_numero_format])

    class Meta:
        model = Client
        fields = ['id', 'numero', 'is_active']
