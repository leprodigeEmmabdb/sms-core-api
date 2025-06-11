import os
import logging
import smpplib.client
import smpplib.consts
import smpplib.gsm
import csv
import re
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

        # Brancher la gestion des DLR (deliver_sm)
        self.client.set_message_received_handler(self.handle_deliver_sm)

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

    def handle_deliver_sm(self, pdu):
        # Cette méthode est appelée à la réception d'un deliver_sm (DLR)
        # pdu.short_message contient le rapport DLR sous forme de texte
        try:
            dlr_text = pdu.params.get('short_message', b'').decode('utf-8', errors='ignore')
            # Extrait les infos du DLR (exemple format SMPP DLR texte)
            # Exemple: id:12345 sub:001 dlvrd:001 submit date:2001011200 done date:2001011201 stat:DELIVRD err:000 text:
            logging.info(f"[DLR RECEIVED] {dlr_text}")

            # Si tu veux parser pour extraire statut et message_id:
            stat = None
            msg_id = None
            parts = dlr_text.split()
            for part in parts:
                if part.startswith('stat:'):
                    stat = part[5:]
                elif part.startswith('id:'):
                    msg_id = part[3:]

            logging.info(f"[DLR PARSED] message_id={msg_id}, status={stat}")
        except Exception as e:
            logging.error(f"Erreur lors du traitement du DLR: {e}")

    def disconnect(self):
        self.client.unbind()
        self.client.disconnect()
        logging.info("Disconnected SMPP client")


def is_valid_phone(number):
    number = number.strip().replace(' ', '').replace('-', '')
    
    if number.startswith('+'):
        number = number[1:]

    if number.startswith('243') and len(number) == 12:
        return number  # Ex: 243844192548

    if len(number) == 9 and not number.startswith('0'):
        return '243' + number  # Ex: 844192548 → 243844192548

    return None  # Numéro invalide

if __name__ == '__main__':
    smpp_client = SmppClient()

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../Q1_2024 Batch 26.csv')
    csv_path = os.path.abspath(csv_path)
    
    cleaned_numbers = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            raw_number = row[0]
            number = raw_number.split(':')[0].strip()
            if is_valid_phone(number):
                cleaned_numbers.append(number)
            else:
                print(f"Numéro invalide ignoré : {number}")

    if cleaned_numbers:
        message = ("Cherchez-vous un Smartphone, Powerbank,chargeur, ordinateur aux meilleurs prix ? "
                   "Rdv chez PKM-SHOP. Av. Colonel Mondjiba 04 ,Ref.rond-point magasin kitambo.")
        smpp_client.send_sms(cleaned_numbers, message)
    else:
        print("Aucun numéro valide trouvé dans le fichier CSV.")