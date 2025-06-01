import os
import smpplib.client
import smpplib.consts
from dotenv import load_dotenv as load_env

load_env()

def send_sms(destinations, message):
    """
    Envoie un SMS à un ou plusieurs destinataires via SMPP.
    Historique complet des actions affiché dans le terminal.
    """

    try:
        print(f"[INFO] Connexion au SMSC {os.environ.get('SMPP_HOST')}:{os.environ.get('SMPP_PORT')}")
        client = smpplib.client.Client(os.environ.get('SMPP_HOST'), int(os.environ.get('SMPP_PORT')))
        client.connect()

        print(f"[INFO] Bind en tant que transmitter (system_id={os.environ.get('SMPP_USERNAME')})")
        client.bind_transmitter(system_id=os.environ.get('SMPP_USERNAME'), password=os.environ.get('SMPP_PASSWORD'))

        if isinstance(destinations, str):
            destinations = [destinations]

        for dest in destinations:
            message_bytes = message.encode('utf-8')

            print(f"[ACTION] Envoi du message à {dest}...")

            pdu = client.send_message(
                source_addr_ton=0x05,  # alphanumérique
                source_addr_npi=0,
                source_addr='PKM-Invest',
                dest_addr_ton=0x02,    # national
                dest_addr_npi=0x01,    # ISDN
                destination_addr=dest,
                short_message=message_bytes,
                data_coding=0,
                registered_delivery=True  # Demander un delivery report
            )

            # ✅ Correction ici
            message_id = pdu.params.get('short_message', 'Non disponible')

            print(f"[SUCCESS] Message envoyé à {dest}")
            print(f"          ➤ Message ID    : {message_id}")
            print(f"          ➤ PDU Status    : {pdu.status}")
            print(f"          ➤ PDU Sequence  : {pdu.sequence}")

        print("[INFO] Fin de session : unbind & disconnect")
        client.unbind()
        client.disconnect()

    except Exception as e:
        print(f"[ERROR] Une erreur est survenue : {str(e)}")

if __name__ == '__main__':
    send_sms('0859415536', 'Hello depuis SMPP avec Python !')
    send_sms(['0859415536', '0852551234'], 'Message broadcast à plusieurs destinataires !')
