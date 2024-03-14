import logging
from dotenv import load_dotenv
import os
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL)

logging.basicConfig(level=logging.INFO)

def get_text_user(message):
    text = ""
    typeMessage = message["type"]

    match typeMessage:
        case "text":
            text = (message["text"])["body"]
        case "interactive":
            interactiveObject = message["interactive"]
            interactiveType = interactiveObject["type"]
            if interactiveType == "button_reply":
                text = (interactiveObject["button_reply"])["title"]
            elif interactiveType == "list_reply":
                text = (interactiveObject["list_reply"])["title"]
            else:
                logging.warning("Interactive type error")
        case _:
            logging.warning("No message")

    return text

def create_message(message_type, number, content=""):
    base_message = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": message_type if message_type not in ("button", "list") else "interactive",
    }

    match message_type:
        case "text":
            base_message["text"] = {"body": content}
        case "image":
            base_message["image"] = {"link": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1dCQ2I8mih5p_nUhSgTLUtiOQONExXS08Bg&usqp=CAU"}  # Asegúrate de que content sea una URL de la imagen
        case "audio":
            base_message["audio"] = {"link": ""}  
        case "video":
            base_message["video"] = {"link": ""} 
        case "document":
            base_message["document"] = {"link": ""} 
        case "location":
            base_message["location"] = {
                "latitude": "4.680218315306055",
                "longitude": "-74.04877443489892",
                "name": "Grupo MOK",
                "address": "Cl. 94a #13 42, Bogotá"
            }
        case "button":
            base_message["interactive"] = {
                "type": "button",
                "body": {
                    "text": "Ya tienes una cuenta?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "001",
                                "title": "Registrarse"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "002",
                                "title": "Iniciar Sesión"
                            }
                        }
                    ]
                }
            }
        case "list":
            base_message["interactive"] = {
                "type": "list",
                "body": {
                    "text": "✅ Tenemos las siguientes opciones:"
                },
                "footer": {
                    "text": "Seleccione una opción"
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                            "title": "Quiero tomar clases de baile!",
                            "rows": [
                                {
                                    "id": "main-buy",
                                    "title": "Grupal",
                                    "description": "Adquirir servicios"
                                },
                                {
                                    "id": "main-sell",
                                    "title": "Personalzado",
                                    "description": "Ofrecer servicios"
                                }
                            ]
                        },
                        {
                            "title": "📍Centro de atención",
                            "rows": [
                                {
                                    "id": "main-agency",
                                    "title": "Acádemia",
                                    "description": "Puedes vicitar nuestra acádemia"
                                },
                                {
                                    "id": "main-contact",
                                    "title": "Asesor",
                                    "description": "Contacta a uno de nuestros asesores"
                                }
                            ]
                        }
                    ]
                }
            }
        case _:
            raise ValueError(f"Unsupported message type: {message_type}")

    return base_message

def insert_sql(texto, number):
    from sqlalchemy import text
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S")
    answer = ""
    try:
        with engine.begin() as connection:
            id_proveedor_result = connection.execute(
                text(f"SELECT id_proveedor FROM proveedores WHERE telefono = '{number}'")
            ).fetchone()
            if id_proveedor_result:
                id_proveedor = id_proveedor_result[0]
                connection.execute(
                    text(f"INSERT INTO mensajes (texto_recibido, fecha_recibido, id_proveedor) VALUES ('{texto}', '{formatted_now}', {id_proveedor})")
                )
                logging.info("Mensaje insertado correctamente en la base de datos.")
            else:
                logging.warning("Proveedor no encontrado para el número de teléfono proporcionado.")
                answer = "Proveedor no encontrado para el número de teléfono proporcionado.\nPor favor, ponerse en contacto con servicio técnico"
    except SQLAlchemyError as e:
        logging.error(f"Error al insertar el mensaje en la base de datos: {e}")
        answer = f"Error al insertar el mensaje en la base de datos: {e}\nPor favor, ponerse en contacto con servicio técnico"

    return answer