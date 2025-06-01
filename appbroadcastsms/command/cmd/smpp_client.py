import os
import smpplib.client
import smpplib.consts
from dotenv import load_dotenv as load_env

load_env()

def send_sms(destinations, message):
    """
    Envoie un SMS à un ou plusieurs destinataires via SMPP.

    :param destinations: str (numéro unique) ou list de str (plusieurs numéros)
    :param message: str, contenu du SMS
    """

    client = smpplib.client.Client(os.environ.get('SMPP_HOST'), int(os.environ.get('SMPP_PORT')))
    client.connect()
    client.bind_transmitter(system_id=os.environ.get('SMPP_USERNAME'), password=os.environ.get('SMPP_PASSWORD'))

    if isinstance(destinations, str):
        destinations = [destinations]

    for dest in destinations:
        # Encoder le message en bytes (utf-8)
        message_bytes = message.encode('utf-8')

        pdu = client.send_message(
            source_addr_ton=0x05,  # alphanumérique
            source_addr_npi=0,
            source_addr='PKM-Invest',
            dest_addr_ton=0x02,    # national
            dest_addr_npi=0x01,    # ISDN
            destination_addr=dest,
            short_message=message_bytes,
            data_coding=0,
        )

        print(f'Message envoyé à {dest}, PDU: {pdu}')

    client.unbind()
    client.disconnect()


if __name__ == '__main__':
    send_sms('0859415536', 'Hello depuis SMPP avec Python !')
    send_sms(['0859415536', '0852551234'], 'Message broadcast à plusieurs destinataires !')
