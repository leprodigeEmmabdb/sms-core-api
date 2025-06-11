# appbroadcastsms/command/cmd/smpp_client.py

import os
import logging
import smpplib.client
import smpplib.consts
import smpplib.gsm
from dotenv import load_dotenv

load_dotenv()

class SmppClient:
    def __init__(self):
        self.host = os.getenv('SMPP_HOST')
        self.port = int(os.getenv('SMPP_PORT'))
        self.system_id = os.getenv('SMPP_USERNAME')
        self.password = os.getenv('SMPP_PASSWORD')
        self.client = smpplib.client.Client(self.host, self.port)
        self.client.connect()
        self.client.bind_transceiver(system_id=self.system_id, password=self.password)
        logging.info(f"Connected and bound to SMPP {self.host}:{self.port} as {self.system_id}")

    def send_sms(self, destinations, message):
        if isinstance(destinations, str):
            destinations = [destinations]

        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message)

        for dest in destinations:
            for part in parts:
                pdu = self.client.send_message(
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

    def disconnect(self):
        self.client.unbind()
        self.client.disconnect()
        logging.info("Disconnected SMPP client")

# Instanciation singleton (à adapter selon le contexte d'utilisation)


if __name__ == '__main__':
    smpp_client = SmppClient()
    smpp_client.send_sms('243844192548', 'Hello depuis SMPP avec Python ! €$£')
    smpp_client.send_sms(['243844192548', '243847038573'], 'Broadcast à plusieurs destinataires avec acc. réception.')
