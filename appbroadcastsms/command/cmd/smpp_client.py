import os
import smpplib.client
import smpplib.consts
from dotenv import load_dotenv as load_env

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

    if isinstance(destinations, str):
        destinations = [destinations]

    for dest in destinations:
        # Encodage message (ici utf-8, adapter selon besoin)
        message_bytes = message.encode('utf-8')
        pdu = client.send_message(
            source_addr_ton=0x05,  # SMPP_TON_ALNUM
            source_addr_npi=0,
            source_addr='PKM-Invest',
            dest_addr_ton=2,       # SMPP_TON_NATIONAL (numéro local)
            dest_addr_npi=1,       # SMPP_NPI_ISDN
            destination_addr=dest,
            short_message=message_bytes,
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
