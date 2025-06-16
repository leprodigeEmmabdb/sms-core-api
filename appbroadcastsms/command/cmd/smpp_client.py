#!/usr/bin/env python3

import os
import logging
import smpplib.client
import smpplib.consts
import smpplib.gsm
import csv
from dotenv import load_dotenv

# Configuration logging
logging.basicConfig(level=logging.INFO)

# Charger les variables d'environnement
load_dotenv()

class SmppClient:
    def __init__(self):
        self.host = os.getenv('SMPP_HOST')
        self.port = int(os.getenv('SMPP_PORT'))
        self.system_id = os.getenv('SMPP_USERNAME')
        self.password = os.getenv('SMPP_PASSWORD')

        self.client = smpplib.client.Client(self.host, self.port)

        # Log quand un message est envoyé avec succès
        self.client.set_message_sent_handler(
            lambda pdu: logging.info(f"[SUBMIT_RESP] seq={pdu.sequence} msgid={pdu.message_id}")
        )

        # Log quand un message est reçu (DLR / MO)
        self.client.set_message_received_handler(self.handle_deliver_sm)

        # Connexion et bind
        self.client.connect()
        self.client.bind_transceiver(system_id=self.system_id, password=self.password)

        logging.info(f"[CONNECTED] Bound to SMPP {self.host}:{self.port} as {self.system_id}")

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
        """
        Handler pour les PDU de type deliver_sm (DLR).
        Extrait les informations du DLR, puis met à jour
        la table Smpp correspondante avec le statut de livraison.
        """
        try:
            # Extraction du message court (statut DLR souvent dans short_message)
            dlr_text = pdu.params.get('short_message', b'').decode('utf-8', errors='ignore')
            logging.info(f"[DLR RECEIVED] {dlr_text}")

            # Initialisation des variables d'extraction
            statut = None
            message_id = None
            erreur = None  # S'il y a un code erreur possible dans le texte (à adapter selon le format DLR)

            # Exemple classique DLR: "id:123456 stat:DELIVRD ..."
            parts = dlr_text.split()
            for part in parts:
                if part.startswith('stat:'):
                    statut = part[5:]
                elif part.startswith('id:'):
                    message_id = part[3:]
                elif part.startswith('err:'):  # Si le DLR a un code erreur
                    erreur = part[4:]

            logging.info(f"[DLR PARSED] message_id={message_id}, statut={statut}, erreur={erreur}")

            if not message_id:
                logging.warning("[DLR WARNING] Pas de message_id trouvé dans DLR, impossible de mettre à jour.")
                return

            # Recherche de l'objet Smpp lié via message_id_smsc
            smpp_obj = Smpp.objects.filter(message_id_smsc=message_id).first()

            if smpp_obj:
                # Mise à jour des champs DLR
                smpp_obj.statut_dlr = statut
                smpp_obj.erreur_dlr = erreur
                smpp_obj.text_dlr = dlr_text
                smpp_obj.date_reception_statut = timezone.now()
                smpp_obj.save()
                logging.info(f"[DLR UPDATED] Enregistrement SMPP {smpp_obj.id} mis à jour avec statut DLR.")
            else:
                logging.warning(f"[DLR WARNING] Aucun enregistrement SMPP trouvé pour message_id={message_id}.")
        except Exception as e:
            logging.error(f"[DLR ERROR] Erreur lors du traitement du DLR: {e}")

    def listen(self):
        try:
            logging.info("[LISTENING] Waiting for DLRs...")
            self.client.listen()
        except KeyboardInterrupt:
            logging.info("[STOPPED] Interrupted by user.")
        finally:
            self.disconnect()

    def disconnect(self):
        try:
            self.client.unbind()
            self.client.disconnect()
            logging.info("[DISCONNECTED] SMPP session closed.")
        except Exception as e:
            logging.warning(f"[DISCONNECT ERROR] {e}")


def is_valid_phone(number):
    number = number.strip().replace(' ', '').replace('-', '')
    if number.startswith('+'):
        number = number[1:]
    if number.startswith('243') and len(number) == 12:
        return number
    if len(number) == 9 or not number.startswith('0'):
        return '243' + number
    return None


if __name__ == '__main__':
    smpp_client = SmppClient()
    try:
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../Q1_2024 Batch 26.csv')
        csv_path = os.path.abspath(csv_path)

        cleaned_numbers = set()

        with open(csv_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                raw_number = row[0]
                number = raw_number.split(':')[0].strip()
                normalized = is_valid_phone(number)
                if normalized:
                    cleaned_numbers.add(normalized)
                else:
                    logging.warning(f"Numéro invalide ignoré : {number}")

        if cleaned_numbers:
            message = "bulk test 1"
            smpp_client.send_sms(list(cleaned_numbers), message)
            smpp_client.listen()
        else:
            logging.warning("Aucun numéro valide trouvé dans le fichier CSV.")
    finally:
        smpp_client.disconnect()
