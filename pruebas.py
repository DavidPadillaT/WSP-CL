
from datetime import datetime

if __name__ == "__main__":
    # Obtener la fecha y hora actuales
    now = datetime.now()

    # Formatear la fecha y hora en el formato deseado
    formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S")

    print(formatted_now)