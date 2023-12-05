import paho.mqtt.client as mqtt
import time
from broadlink44a import sendmessage44 as sender44


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("mqtttest")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    sender44.send1("testing")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace 'your-broker-address' with your MQTT broker address
client.connect("0.0.0.0", 1883, 60)

# Start the MQTT loop in the background
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()
