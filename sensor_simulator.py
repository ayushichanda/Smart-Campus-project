import paho.mqtt.client as mqtt
import random
import json
import time

broker = "localhost"

energy_topic = "campus/energy"
alert_topic = "campus/alert"

client = mqtt.Client()
client.connect(broker)

rooms = [
    "Physics Lab",
    "Chemistry Lab",
    "CS Lab",
    "Electronics Lab",
    "Mechanical Workshop",
    "Auditorium"
]

while True:

    room = random.choice(rooms)

    temperature = random.randint(24, 40)
    power = random.randint(100, 500)

    occupancy = random.choice([0,1])   # moved here

    data = {
        "room": room,
        "temperature": temperature,
        "power": power,
        "occupancy": occupancy
    }

    # publish energy data
    client.publish(energy_topic, json.dumps(data))
    print("Energy Data:", data)

    # temperature alert
    if temperature > 35:
        alert_msg = {
            "alert": f"HIGH TEMPERATURE in {room}: {temperature}C"
        }
        client.publish(alert_topic, json.dumps(alert_msg))
        print("ALERT:", alert_msg)

    # power alert
    if power > 420:
        alert_msg = {
            "alert": f"HIGH POWER usage in {room}: {power}W"
        }
        client.publish(alert_topic, json.dumps(alert_msg))
        print("ALERT:", alert_msg)

    time.sleep(30)