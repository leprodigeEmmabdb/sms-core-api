# appbroadcastsms/vues/sms/views.py

import pandas as pd
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from appbroadcastsms.command.cmd.smpp_client import send_sms

from appbroadcastsms.models import Sms
from appbroadcastsms.vues.sms.sz_sms import (
    AddSmsSerializer,
    SendFileSmsSerializer,
    UpdateSmsSerializer,
    SmsSerializer,
    SendSingleSmsSerializer,
    SendBroadcastMessageSerializer
)


class SmsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Sms.objects.all()

    def get_serializer_class(self):
        if self.action == 'send_single_sms':
            return SendSingleSmsSerializer
        elif self.action == 'send_bulk_sms':
            return SendBroadcastMessageSerializer
        elif self.request.method == 'POST':
            return AddSmsSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UpdateSmsSerializer
        return SmsSerializer

    @action(detail=False, methods=['post'], url_path='send-single')
    def send_single_sms(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            result = send_sms(data['receiver'], data['message'])
            print(f"Result of sending SMS: {result}")  # Debugging line to check the result
            return Response(result, status=status.HTTP_200_OK if result else 500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='send-bulk')
    def send_bulk_sms(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = send_sms(data['receivers'], data['message'])
            return Response(result, status=status.HTTP_200_OK if result['status'] == 'success' else 500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='send-from-file')
    def send_from_file(self, request):
        serializer = SendFileSmsSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            file = serializer.validated_data['file']

            try:
                # Lire les numéros depuis le fichier (XLSX ou CSV)
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                # On suppose que la colonne contenant les numéros s'appelle 'receiver'
                if 'receiver' not in df.columns:
                    return Response({"error": "Colonne 'receiver' non trouvée."}, status=400)

                receivers = df['receiver'].dropna().astype(str).tolist()

                # Tu peux aussi filtrer ici avec `validate_rdc_number` si tu veux
                if not receivers:
                    return Response({"error": "Aucun numéro valide trouvé."}, status=400)

                result = send_sms(receivers, message)
                return Response(result, status=200 if result['status'] == 'success' else 500)

            except Exception as e:
                return Response({"error": f"Erreur lors du traitement du fichier: {str(e)}"}, status=500)

