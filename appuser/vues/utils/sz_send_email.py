from django.contrib.auth import forms
from django.core.mail import send_mail
from rest_framework import serializers

from app_user.models import Departements, UserPostes, Agent, User
from app_user.vues.user.user_sz import DjoserCurrentUserSerializer


class SendEmailSZ(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()
    expediteur = serializers.EmailField(initial="info@bcru.local",
                                        )
    destinataire = serializers.EmailField()

    # class Meta:
    #     fields = "__all__"

    def save(self, **data):
        send_mail("subject", "Hello", "info@perf.local", ['admin@perf.local'])
        return dict(msg="Email sent")
