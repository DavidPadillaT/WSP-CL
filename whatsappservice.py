import requests
import json
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("WHATSAPP_API_TOKEN")
API_URL = os.getenv("WHATSAPP_API_URL")

def send_message_whatsapp(base_message):
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}
        
        response = requests.post(API_URL, data=json.dumps(base_message), headers=headers)
        
        if response.status_code == 200:
            logging.info("Message sent successfully.")
            return True
        else:
            logging.error(f"Failed to send message: {response.text}")
            return False
    except requests.exceptions.RequestException as exception:
        logging.error(f"Request exception: {exception}")
        return False