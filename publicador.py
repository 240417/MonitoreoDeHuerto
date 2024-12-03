
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime
import json

BROKER = 'test.mosquitto.org'
PORT = 1883

# Información de ejemplo para la estructura
BUILDING = "edificio_1"
FLOOR = "piso_1"
ROOM = "Area_1"
CONTROL_SYSTEM = "HVAC"
DEVICE = "sensor"
ALERT_TYPE = "temperature_alert"

# Estructura de Tópicos de acuerdo con la jerarquía solicitada
TOPICS = {
    "temperature": f"building/{BUILDING}/{FLOOR}/{ROOM}/temperature",
    "humidity": f"building/{BUILDING}/{FLOOR}/{ROOM}/humidity",
    "pressure": f"building/{BUILDING}/{FLOOR}/{ROOM}/pressure",
    "light": f"building/{BUILDING}/{FLOOR}/{ROOM}/light",
    "control": f"control/{BUILDING}/{CONTROL_SYSTEM}/{DEVICE}",
    "alerts": f"alerts/{BUILDING}/{ALERT_TYPE}",
    "device_status": f"control/{BUILDING}/{CONTROL_SYSTEM}/{DEVICE}/status",
    "sensor_readings": f"control/{BUILDING}/{CONTROL_SYSTEM}/{DEVICE}/sensor_readings",
    "system_configuration": f"control/{BUILDING}/{CONTROL_SYSTEM}/configuration",
    "alert_thresholds": f"control/{BUILDING}/{CONTROL_SYSTEM}/alert_thresholds"
}

# Valores de umbral para alertas
alert_thresholds = {
    "temperature": 25.0,
    "humidity": 50.0,
    "pressure": 1015.0,
    "light": 500
}

def publish_sensor_data(client):
    while True:
        # Generamos datos aleatorios para los sensores
        data = {
            "temperature": round(random.uniform(20, 60), 2),
            "humidity": round(random.uniform(10, 120), 2),
            "pressure": round(random.uniform(1010, 1020), 2),
            "light": round(random.uniform(300, 800), 2),
        }

        # Publicamos los datos en los tópicos con formato JSON
        for key, topic in TOPICS.items():
            # Los datos de los sensores solo se publican en sus tópicos específicos
            if key in data:
                message = json.dumps({
                    "value": data[key],
                    
                    "timestamp": time.time()
                })
                retain_flag = False
            else:
                # Para control y alertas, los mensajes pueden ser genéricos
                if key == "device_status":
                    message = json.dumps({
                        "status": "active",  # Suponiendo que el dispositivo está activo
                        "timestamp": time.time()
                    })
                    retain_flag = True  # Retain flag para el estado del dispositivo

                elif key == "sensor_readings":
                    # Últimas lecturas de sensores críticos
                    message = json.dumps({
                        "temperature": data["temperature"],
                        "humidity": data["humidity"],
                        "pressure": data["pressure"],
                        "light": data["light"],
                        "timestamp": time.time()
                    })
                    retain_flag = True  # Retain flag para las últimas lecturas

                elif key == "system_configuration":
                    # Configuración del sistema
                    system_config = {
                        "sampling_interval": 5,  # Intervalo de muestreo de 5 segundos
                        "sensor_types": ["temperature", "humidity", "pressure", "light"]
                    }
                    message = json.dumps(system_config)
                    retain_flag = True  # Retain flag para la configuración

                elif key == "alert_thresholds":
                    # Umbrales de alerta para sensores
                    message = json.dumps(alert_thresholds)
                    retain_flag = True  # Retain flag para los umbrales de alerta

            # Publicar con retain flag según corresponda
            client.publish(topic, message, retain=retain_flag)
            print(f"Publicado en {topic}: {message}")

        time.sleep(15)

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    publish_sensor_data(client)

if __name__ == "__main__":
    main()
