#!/usr/bin/python

import os
import time
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
    if hasattr(pdu, 'receipted_message_id'):
        msg = f"[DLR] Reçu pour msgid: {pdu.receipted_message_id}"
    else:
        msg = f"[DELIVER_SM] Message reçu: {pdu.short_message.decode(errors='ignore')}"
    logging.info(msg)
    print(msg)
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

        msg = f"[INFO] Connexion à {host}:{port}"
        logging.info(msg)
        print(msg)

        client = smpplib.client.Client(host, port)

        client.set_message_sent_handler(
            lambda pdu: (
                logging.info(f"[SENT] submit_sm_resp seqno={pdu.sequence}, msgid={pdu.message_id}"),
                print(f"[SENT] submit_sm_resp seqno={pdu.sequence}, msgid={pdu.message_id}")
            )
        )
        client.set_message_received_handler(handle_deliver_sm)

        client.connect()

        msg = f"[INFO] Bind en tant que transceiver (system_id={system_id})"
        logging.info(msg)
        print(msg)
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
                log_msg = f"[SEND] ➤ Dest={dest} | Seq={pdu.sequence} | Status={pdu.status}"
                logging.info(log_msg)
                print(log_msg)

        # Attente active pour les accusés de réception (DLR)
        logging.info("[INFO] En attente des accusés de réception (DLR)...")
        print("[INFO] En attente des accusés de réception (DLR)...")
        for _ in range(10):  # ~10 secondes
            client.read_once()
            time.sleep(1)

        logging.info("[INFO] Fin de session : unbind & disconnect")
        print("[INFO] Fin de session : unbind & disconnect")
        client.unbind()
        client.disconnect()

    except Exception as e:
        err_msg = f"[ERROR] {str(e)}"
        logging.error(err_msg)
        print(err_msg)

if __name__ == '__main__':
    send_sms('243844192548', 'Hello depuis SMPP avec Python ! €$£')
    send_sms(['243844192548', '243847038573'], 'Broadcast à plusieurs destinataires avec acc. réception.')
