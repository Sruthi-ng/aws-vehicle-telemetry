import time
import json
import random
import uuid
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# --- CONFIGURATION (UPDATE THESE!) ---
ENDPOINT = "a1eydhch2gmav5-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "SimulatedVehicle_01"
# Update these filenames to match exactly what you downloaded
PATH_TO_CERT = "certs/a4b9938c44fb7221884e1d82d58a82d63d12fc8746131f20068684a648249b1e-certificate.pem.crt"
PATH_TO_KEY = "certs/a4b9938c44fb7221884e1d82d58a82d63d12fc8746131f20068684a648249b1e-private.pem.key"
PATH_TO_ROOT = "certs/AmazonRootCA1.pem"
TOPIC = "vehicle/telemetry"

def generate_vehicle_data():
    # Simulation Logic: 10% chance of overheating
    is_overheating = random.random() > 0.90 
    coolant_temp = random.randint(106, 125) if is_overheating else random.randint(85, 102)
    speed = random.randint(0, 220)
    rpm = random.randint(800, 1500) if speed == 0 else random.randint(1500, 7000)

    payload = {
        "metadata": {
            "vehicle_id": CLIENT_ID,
            "timestamp": int(time.time())
        },
        "powertrain": {
            "engine_rpm": rpm,
            "vehicle_speed_kmh": speed,
            "engine_coolant_temp_c": coolant_temp,
            "battery_voltage_v": round(random.uniform(13.5, 14.8), 2)
        },
        "diagnostics": {
            "mil_status": "ON" if is_overheating else "OFF"
        }
    }
    return payload

# --- MAIN EXECUTION ---
print("Initializing Vehicle Simulator...")
myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

print("Connecting to AWS IoT Core...")
myMQTTClient.connect()
print("Connected! Sending data...")

try:
    while True:
        data = generate_vehicle_data()
        payload = json.dumps(data)
        print(f"Sent Temp: {data['powertrain']['engine_coolant_temp_c']}°C")
        myMQTTClient.publish(TOPIC, payload, 1)
        time.sleep(5) 
except KeyboardInterrupt:
    myMQTTClient.disconnect()