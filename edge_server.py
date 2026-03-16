import paho.mqtt.client as mqtt
import json
import sqlite3

broker = "localhost"
port = 1883

topic = "campus/energy"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    room = data["room"]
    temperature = data["temperature"]
    power = data["power"]
    occupancy = data["occupancy"]   # NEW

    # status logic
    if occupancy == 0 and power > 200:
        status = "ENERGY WASTE"
    elif temperature > 30 or power > 400:
        status = "ALERT"
    else:
        status = "NORMAL"

    print("--------------------------------")
    print("Room:", room)
    print("Temperature:", temperature)
    print("Power:", power)
    print("Occupancy:", occupancy)
    print("Status:", status)

    conn = sqlite3.connect("campus_energy.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO energy_data (room, temperature, power, status) VALUES (?, ?, ?, ?)",
        (room, temperature, power, status)
    )

    conn.commit()
    conn.close()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)

client.loop_forever()