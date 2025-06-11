#!/usr/bin/python

import os
import logging
import time
from dotenv import load_dotenv
import smpplib.client
import smpplib.consts
import smpplib.gsm

load_dotenv()

# Mapping des codes d'erreur SMPP
SMPP_STATUS_CODES = {
    0x00000000: "ESME_ROK - No Error",
    0x00000001: "ESME_RINVMSGLEN - Message Length is invalid",
    0x00000002: "ESME_RINVCMDLEN - Command Length is invalid",
    0x00000003: "ESME_RINVCMDID - Invalid Command ID",
    0x00000004: "ESME_RINVBNDSTS - Incorrect BIND Status for given command",
    0x00000005: "ESME_RALYBND - ESME Already in Bound State",
    0x00000006: "ESME_RINVPRTFLG - Invalid Priority Flag",
    0x00000007: "ESME_RINVREGDLVFLG - Invalid Registered Delivery Flag",
    0x00000008: "ESME_RSYSERR - System Error",
    0x0000000A: "ESME_RINVSRCADR - Invalid Source Address",
    0x0000000B: "ESME_RINVDSTADR - Invalid Destination Address",
    0x0000000C: "ESME_RINVMSGID - Message ID is invalid",
    0x0000000D: "ESME_RBINDFAIL - Bind Failed",
    0x0000000E: "ESME_RINVPASWD - Invalid Password",
    0x0000000F: "ESME_RINVSYSID - Invalid System ID",
    0x00000011: "ESME_RCANCELFAIL - Cancel SM Failed",
    0x00000013: "ESME_RREPLACEFAIL - Replace SM Failed",
    0x00000014: "ESME_RMSGQFUL - Message Queue Full",
    0x00000015: "ESME_RINVSERTYP - Invalid Service Type",
    0x00000033: "ESME_RINVNUMDESTS - Invalid number of destinations",
    0x00000034: "ESME_RINVDLNAME - Invalid Distribution List name",
    0x00000040: "ESME_RINVDESTFLAG - Destination flag is invalid",
    0x00000042: "ESME_RINVSUBREP - Invalid ‘submit with replace’ request",
    0x00000043: "ESME_RINVESMCLASS - Invalid esm_class field data",
    0x00000044: "ESME_RCNTSUBDL - Cannot Submit to Distribution List",
    0x00000045: "ESME_RSUBMITFAIL - submit_sm or submit_multi failed",
    0x00000048: "ESME_RINVSRCTON - Invalid Source address TON",
    0x00000049: "ESME_RINVSRCNPI - Invalid Source address NPI",
    0x00000050: "ESME_RINVDSTTON - Invalid Destination address TON",
    0x00000051: "ESME_RINVDSTNPI - Invalid Destination address NPI",
    0x00000053: "ESME_RINVSYSTYP - Invalid system_type field",
    0x00000054: "ESME_RINVREPFLAG - Invalid replace_if_present flag",
    0x00000055: "ESME_RINVNUMMSGS - Invalid number of messages",
    0x00000058: "ESME_RTHROTTLED - Throttling error (message rate too high)",
    0x00000061: "ESME_RINVSCHED - Invalid Scheduled Delivery Time",
    0x00000062: "ESME_RINVEXPIRY - Invalid message validity period",
    0x00000063: "ESME_RINVDFTMSGID - Predefined Message ID is invalid",
    0x00000064: "ESME_RX_T_APPN - ESME Receiver Temporary App Error Code",
    0x00000065: "ESME_RX_P_APPN - ESME Receiver Permanent App Error Code",
    0x00000066: "ESME_RX_R_APPN - ESME Receiver Reject Message Error Code",
    0x00000067: "ESME_RQUERYFAIL - query_sm request failed",
    0x000000C0: "ESME_RINVTLVSTREAM - Error in optional part of PDU body",
    0x000000C1: "ESME_RTLVNOTALLWD - TLV not allowed",
    0x000000C2: "ESME_RINVTLVLEN - Invalid Parameter Length",
    0x000000C3: "ESME_RMISSINGTLV - Expected TLV missing",
    0x000000C4: "ESME_RINVTLVVAL - Invalid TLV Value",
    0x000000FE: "ESME_RDELIVERYFAILURE - Delivery Failure (used by some vendors)",
    0x000000FF: "ESME_RUNKNOWNERR - Unknown Error"
}

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def handle_deliver_sm(pdu):
    """Callback pour traiter les accusés de réception"""
    try:
        short_message = pdu.params.get('short_message', b'').decode(errors='ignore')
        logging.info(f"[DLR] ➤ From SMSC: {short_message}")
    except Exception as e:
        logging.error(f"[DLR] ➤ Erreur lors du traitement du DLR: {str(e)}")
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

                status_text = SMPP_STATUS_CODES.get(pdu.status, "Unknown Status Code")
                log_msg = f"[SEND] ➤ Dest={dest} | Seq={pdu.sequence} | Status={pdu.status} ({status_text})"
                logging.info(log_msg)
                print(log_msg)

        logging.info("[INFO] Attente des DLR pendant 15 secondes...")
        start = time.time()
        while time.time() - start < 15:
            client.read_once()
            time.sleep(0.2)

        logging.info("[INFO] Fin de session : unbind & disconnect")
        print("[INFO] Fin de session : unbind & disconnect")
        client.unbind()
        client.disconnect()

    except Exception as e:
        logging.error(f"[ERROR] {str(e)}")

if __name__ == '__main__':
    send_sms('0844192548', 'Hello depuis SMPP avec Python ! €$£')
    send_sms(['0844192548', '0844192548'], 'Broadcast à plusieurs destinataires avec acc. réception.')