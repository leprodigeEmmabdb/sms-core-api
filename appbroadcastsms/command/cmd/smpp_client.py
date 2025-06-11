#!/usr/bin/python

import os
import logging
from dotenv import load_dotenv
import smpplib.client
import smpplib.consts
import smpplib.gsm

load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def handle_deliver_sm(pdu):
    """Callback pour traiter les accusés de réception"""
    logging.info(f"[DLR] Reçu pour msgid: {pdu.receipted_message_id}")
    return 0

def send_sms(destinations, message):
    """
    Envoie un SMS (ou multi-part) à un ou plusieurs destinataires via SMPP.
    """
    try:
        host = os.getenv('SMPP_HOST')
        port = int(os.getenv('SMPP_PORT'))
        system_id = os.getenv('SMPP_USERNAME')
        password = os.getenv('SMPP_PASSWORD')

        logging.info(f"[INFO] Connexion à {host}:{port}")
        client = smpplib.client.Client(host, port)

        client.set_message_sent_handler(
            lambda pdu: logging.info(f"[SENT] submit_sm_resp seqno={pdu.sequence}, msgid={pdu.message_id}")
        )
        client.set_message_received_handler(handle_deliver_sm)

        client.connect()
        logging.info(f"[INFO] Bind en tant que transceiver (system_id={system_id})")
        print(f"[INFO] Bind en tant que transceiver (system_id={system_id})")
        client.bind_transceiver(system_id=system_id, password=password)

        if isinstance(destinations, str):
            destinations = [destinations]

        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message)

        for dest in destinations:
            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                    source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
                    source_addr='PKM-Invest',

                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    destination_addr=dest,

                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True
                )
                logging.info(f"[SEND] ➤ Dest={dest} | Seq={pdu.sequence} | Status={pdu.status}")
                print(f"[SEND] ➤ Dest={dest} | Seq={pdu.sequence} | Status={pdu.status}")

        logging.info("[INFO] Fin de session : unbind & disconnect")
        print("[INFO] Fin de session : unbind & disconnect")
        client.unbind()
        client.disconnect()

    except Exception as e:
        logging.error(f"[ERROR] {str(e)}")

if __name__ == '__main__':
    send_sms('0844192548', 'Hello depuis SMPP avec Python ! €$£')
    send_sms(['0844192548', '0844192548'], 'Broadcast à plusieurs destinataires avec acc. réception.')
