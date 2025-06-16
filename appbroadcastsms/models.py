
from django.db import models
from root.utils.model_utils import ModelMixin
from django_countries.fields import CountryField


# Create your models here.


class Client(ModelMixin):
    numero = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "tb_clients"

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
    
    # Code de retour du SMSC après envoi (submit_sm_resp)
    code_retour = models.CharField(max_length=20, null=True, blank=True)
    # ID du message attribué par le SMSC (submit_sm_resp)
    message_id_smsc = models.CharField(max_length=100, null=True, blank=True)

    # Statut final retourné par le DLR (deliver_sm)
    statut_dlr = models.CharField(max_length=20, null=True, blank=True)
    # Code d'erreur retourné par le DLR
    code_erreur_dlr = models.CharField(max_length=10, null=True, blank=True)

    # Date d'envoi réelle du message (souvent dans le DLR sous submit date)
    date_envoi = models.DateTimeField(null=True, blank=True)
    # Date à laquelle le SMS a été livré ou un statut final a été attribué (done date)
    date_livraison = models.DateTimeField(null=True, blank=True)

    # Date où le DLR a été reçu sur le client SMPP (date de réception du rapport)
    date_reception_statut = models.DateTimeField(null=True, blank=True)

    # Texte brut complet du DLR reçu (utile pour debug ou analyse détaillée)
    dlr_texte_brut = models.TextField(null=True, blank=True)

    # Horodatage de la création et dernière mise à jour en base
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
         db_table = "tb_smpp"
    def __str__(self):
        return f"Envoi msg {self.message.id} à client {self.client.numero}"