import paho.mqtt.client as mqtt
import json

BROKER = 'test.mosquitto.org'
PORT = 1883

# Tópico general con wildcard para escuchar todos los datos de sensores, control, alertas, etc.
#TOPIC = "building/+/+/+/+"  # Escucha cualquier sensor en cualquier edificio, piso, habitación
TOPICS = [
    "building/+/+/+/+",                     # Monitoreo general
    "building/+/piso_1/+/+",                # Monitoreo por piso
    "building/+/+/+/temperature",           # Monitoreo por tipo de sensor: temperatura
    "alerts/+/+",                           # Monitoreo de alertas
    "control/+/hvac/#"                      # Sistema de control HVAC
]
# Función de conexión
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código {rc}")
    # Suscribirse a los tópicos con wildcard
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"Suscrito al tópico: {topic}")

# Función de manejo de mensajes recibidos
def on_message(client, userdata, msg):
    try:
        # Decodificar el mensaje JSON
        payload = json.loads(msg.payload.decode())
        
        print(f"Mensaje recibido - {msg.topic}:")
        print(json.dumps(payload, indent=2))
        
        # Verificar si el payload es un diccionario antes de buscar claves
        if isinstance(payload, dict):
            if 'temperature' in payload and isinstance(payload['temperature'], (int, float)):
                if payload['temperature'] > 25.0:
                    print("¡Alerta! Temperatura superior al umbral.")
            elif 'humidity' in payload and isinstance(payload['humidity'], (int, float)):
                if payload['humidity'] > 50.0:
                    print("¡Alerta! Humedad superior al umbral.")
        else:
            print(f"Payload inesperado: {payload}")
                  
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON: {msg.payload.decode()}")

# Función principal
def main():
    client = mqtt.Client()
    
    # Asignar las funciones de conexión y mensaje
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar al broker
    client.connect(BROKER, PORT)

    # Ejecutar el loop para escuchar mensajes
    client.loop_forever()

if __name__ == "__main__":
    main()
