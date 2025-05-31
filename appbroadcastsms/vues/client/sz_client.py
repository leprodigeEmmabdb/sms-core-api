from rest_framework import serializers

from appbroadcastsms.models import Client



# Serializers define the API representation.

class SimpleClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "numero"]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

class AddClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = ["id", "numero"]


class UpdateClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = ["id", "numero","is_active"]
