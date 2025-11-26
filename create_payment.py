<<<<<<< HEAD
import os
import requests
from dotenv import load_dotenv
import uuid
import json

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración (Corregida según la documentación de la API v3) ---
KHIPU_API_KEY = os.getenv("KHIPU_API_KEY")
KHIPU_API_URL = "https://payment-api.khipu.com/v3/payments"

# URL pública de tu webhook (puedes usar ngrok para pruebas locales)
# Ejemplo: https://tunel-de-ngrok.ngrok.io/api/khipu/webhook
WEBHOOK_URL = "https://2ea1916ed0cc.ngrok-free.app/api/khipu/webhook" 

if not KHIPU_API_KEY or KHIPU_API_KEY == "TU_CLAVE_SECRETA_API":
    print("Error: Debes configurar tu KHIPU_API_KEY en el archivo .env")
    exit()

# --- Datos del Pago (Dummy, en formato JSON) ---
datos_pago = {
    'subject': 'Producto de Prueba',
    'amount': 100, # Monto como número
    'currency': 'CLP',
    'transaction_id': str(uuid.uuid4()), # ID de transacción único
    'body': 'Descripción del producto de prueba',
    'notifyUrl': WEBHOOK_URL, # Corregido a camelCase
    'returnUrl': 'http://mi-tienda.com/pago/exitoso', # Corregido a camelCase
    'cancelUrl': 'http://mi-tienda.com/pago/cancelado', # Corregido a camelCase
    # 'notify_api_version' no es necesario en la API v3, la versión está en la URL
}

# --- Cabeceras de la Petición (Corregidas) ---
headers = {
    'x-api-key': KHIPU_API_KEY,
    'Content-Type': 'application/json'
}

# --- Creación del Pago ---
try:
    print("Creando enlace de pago en Khipu (API v3)...")
    # Se usa 'json=datos_pago' para enviar el cuerpo como application/json
    response = requests.post(KHIPU_API_URL, json=datos_pago, headers=headers)
    response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

    respuesta_json = response.json()
    
    payment_id = respuesta_json.get('payment_id') # Corregido a snake_case según la respuesta real
    payment_url = respuesta_json.get('payment_url') # Corregido a snake_case según la respuesta real

    if payment_url:
        print("\n--- ¡Enlace de Pago Creado Exitosamente! ---")
        print(f"ID del Pago: {payment_id}")
        print(f"URL de Pago: {payment_url}")
        print("Puedes abrir esta URL en tu navegador para simular el pago con una cuenta de desarrollador.")
    else:
        print("\nError: No se pudo obtener la URL de pago de la respuesta.")
        print("Respuesta recibida:", respuesta_json)

except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
    print(f"Cuerpo de la respuesta: {errh.response.text}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Error de Timeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Ocurrió un error: {err}")
=======
import os
import requests
from dotenv import load_dotenv
import uuid
import json

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración (Corregida según la documentación de la API v3) ---
KHIPU_API_KEY = os.getenv("KHIPU_API_KEY")
KHIPU_API_URL = "https://payment-api.khipu.com/v3/payments"

# URL pública de tu webhook (puedes usar ngrok para pruebas locales)
# Ejemplo: https://tunel-de-ngrok.ngrok.io/api/khipu/webhook
WEBHOOK_URL = "https://2ea1916ed0cc.ngrok-free.app/api/khipu/webhook" 

if not KHIPU_API_KEY or KHIPU_API_KEY == "TU_CLAVE_SECRETA_API":
    print("Error: Debes configurar tu KHIPU_API_KEY en el archivo .env")
    exit()

# --- Datos del Pago (Dummy, en formato JSON) ---
datos_pago = {
    'subject': 'Producto de Prueba',
    'amount': 100, # Monto como número
    'currency': 'CLP',
    'transaction_id': str(uuid.uuid4()), # ID de transacción único
    'body': 'Descripción del producto de prueba',
    'notifyUrl': WEBHOOK_URL, # Corregido a camelCase
    'returnUrl': 'http://mi-tienda.com/pago/exitoso', # Corregido a camelCase
    'cancelUrl': 'http://mi-tienda.com/pago/cancelado', # Corregido a camelCase
    # 'notify_api_version' no es necesario en la API v3, la versión está en la URL
}

# --- Cabeceras de la Petición (Corregidas) ---
headers = {
    'x-api-key': KHIPU_API_KEY,
    'Content-Type': 'application/json'
}

# --- Creación del Pago ---
try:
    print("Creando enlace de pago en Khipu (API v3)...")
    # Se usa 'json=datos_pago' para enviar el cuerpo como application/json
    response = requests.post(KHIPU_API_URL, json=datos_pago, headers=headers)
    response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

    respuesta_json = response.json()
    
    payment_id = respuesta_json.get('payment_id') # Corregido a snake_case según la respuesta real
    payment_url = respuesta_json.get('payment_url') # Corregido a snake_case según la respuesta real

    if payment_url:
        print("\n--- ¡Enlace de Pago Creado Exitosamente! ---")
        print(f"ID del Pago: {payment_id}")
        print(f"URL de Pago: {payment_url}")
        print("Puedes abrir esta URL en tu navegador para simular el pago con una cuenta de desarrollador.")
    else:
        print("\nError: No se pudo obtener la URL de pago de la respuesta.")
        print("Respuesta recibida:", respuesta_json)

except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
    print(f"Cuerpo de la respuesta: {errh.response.text}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Error de Timeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Ocurrió un error: {err}")
>>>>>>> 8ccd15582954fdb03959ebeffec6ff339ed5b2c1
