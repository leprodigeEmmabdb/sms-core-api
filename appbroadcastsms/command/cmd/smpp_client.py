import os
import smpplib.client
import smpplib.consts
from dotenv import load_dotenv as load_env

# Charger les variables d'environnement depuis le fichier .env
load_env()

def send_sms(destinations, message):
    """
    Envoie un SMS à un ou plusieurs destinataires.

    :param destinations: str (numéro unique) ou list de str (plusieurs numéros)
    :param message: str, contenu du SMS
    """

    client = smpplib.client.Client(os.environ.get('SMPP_HOST'), int(os.environ.get('SMPP_PORT')))
    client.connect()
    client.bind_transmitter(system_id=os.environ.get('SMPP_USERNAME'), password=os.environ.get('SMPP_PASSWORD'))

    # Si destinations est un str, on le transforme en liste pour uniformiser la boucle
    if isinstance(destinations, str):
        destinations = [destinations]

    for dest in destinations:
        pdu = client.send_message(
            source_addr_ton=0x05,  # Nom expéditeur alphanumérique
            source_addr_npi=0,
            source_addr='PKM-Invest',  # Nom expéditeur
            dest_addr_ton=2,
            dest_addr_npi=1,
            destination_addr=dest,
            short_message=message,
            data_coding=0,
        )
        print(f'Message envoyé à {dest}, PDU: {pdu}')

    client.unbind()
    client.disconnect()


if __name__ == '__main__':
    # Exemple d'envoi à un seul numéro
    send_sms('33612345678', 'Hello depuis SMPP avec Python !')

    # Exemple d'envoi à plusieurs numéros
    send_sms(['33612345678', '33798765432'], 'Message broadcast à plusieurs destinataires !')
