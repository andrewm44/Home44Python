# Introduction 
Simple Python tasks for Home44 Portal, mostly around device control

A key element is the use of MQTT, via Mosquitto Broker

Also lifted code for managing remote controls via a Broadlink device form python-broadlink

# Mosquitto install

```
sudo apt install -y mosquitto mosquitto-clients
```

and 
```
sudo systemctl enable mosquitto.service
```

test using a client from Windows
[MQTTX](https://mqttx.app/)


then create a Python daemon to listen for messages

use the library paho-mqtt

and try this script
```
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("your/topic")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace 'your-broker-address' with your MQTT broker address
client.connect("your-broker-address", 1883, 60)

# Start the MQTT loop in the background
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()

```


THEN:

```
pip install broadlink
```


in .Net - 

[MQTTnet](https://github.com/dotnet/MQTTnet)