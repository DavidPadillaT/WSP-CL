from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging
import util
import whatsappservice

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

@app.route('/welcome', methods=['GET'])
def index():
    return "Welcome developer! This versión 0.0.1 of Clave Latina WhatsApp API"

@app.route('/whatsapp', methods=['GET'])
def verify_token():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token and challenge and token == ACCESS_TOKEN:
        return challenge
    else:
        logging.warning("Failed token verification.")
        return jsonify({"error": "Validation failed"}), 400

@app.route('/whatsapp', methods=['POST'])
def receive_message():
    body = request.get_json()
    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        number = message["from"]
        text = util.get_text_user(message).lower()
        process_messages(text, number)
        return "EVENT RECEIVED"
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({"error": "Bad request"}), 400

def process_messages(text, number):

    list_data = []
    whatsappservice.send_message_whatsapp(util.create_message("text", number, text))
    
    if (text == "sí") or (text == "no"):
        list_data.append(util.create_message("text", number, "Recibiendo su respuesta.\nPor favor, espere..."))
        answer = util.insert_sql(text, number)
        if answer != "":
            list_data.append(util.create_message("text", number, answer))
    elif "hola" in text:
        list_data.append(util.create_message("text", number, "Hola! Cómo estás? Soy Yury. Cómo puedo ayudarte?"))
        list_data.append(util.create_message("list", number))
    elif "gracias" in text:
        list_data.append(util.create_message("text", number, "Gracias por contactarnos, feliz día!"))
    elif "oficina" in text:
        list_data.append(util.create_message("text", number, "Estas son nuestras oficinas"))
        list_data.append(util.create_message("location", number))
        list_data.append(util.create_message("image", number))
        list_data.append(util.create_message("text", number, "Te esperamos!"))
        list_data.append(util.create_message("text", number, "Algo más en lo que pueda ayudarte?"))
        list_data.append(util.create_message("list", number))
    elif "contacto" in text:
        list_data.append(util.create_message("text", number, "*Número de contacto:*\n6016283600"))
        list_data.append(util.create_message("text", number, "Algo más en lo que pueda ayudarte?"))
        list_data.append(util.create_message("list", number))
    elif ("cliente" in text) or ("proveedor" in text):
        list_data.append(util.create_message("button", number))
    elif "registrarse" in text:
        list_data.append(util.create_message("text", number, "Por favor, ingresa a este link para registrarte: https://www.grupomok.com/"))
    elif "iniciar sesión" in text:
        list_data.append(util.create_message("text", number, "Por favor, ingresa a este link para iniciar sesión: https://www.grupomok.com/"))
    else:
        list_data.append(util.create_message("text", number, "Lo siento, no pude entenderte..."))
        list_data.append(util.create_message("text", number, "Algo más en lo que pueda ayudarte?"))
        list_data.append(util.create_message("list", number))

    for item in list_data:
        whatsappservice.send_message_whatsapp(item)

if __name__ == "__main__":
    app.run(debug=True)