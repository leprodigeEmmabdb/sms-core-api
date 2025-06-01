
from django.db import models
from root.utils.model_utils import ModelMixin
from django_countries.fields import CountryField


# Create your models here.


class Client(ModelMixin):
    numero = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "tb_client"

    def __str__(self):
        return f"{self.numero}"
    
class Sms(ModelMixin):
    message = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "tb_sms"

    def __str__(self):
        return f"{self.message}"

class Smpp(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='smpp')
    message = models.ForeignKey(Sms, on_delete=models.CASCADE, related_name='smpp')
    code_retour = models.CharField(max_length=20, null=True, blank=True)       # code retour SMPP
    message_id_smsc = models.CharField(max_length=100, null=True, blank=True)  # ID message SMPP retourné par SMSC
    date_reception_statut = models.DateTimeField(null=True, blank=True)        # date du dernier statut DLR

    class Meta:
        pass
    def __str__(self):
        return f"Envoi msg {self.message.id} à client {self.client.numero}"