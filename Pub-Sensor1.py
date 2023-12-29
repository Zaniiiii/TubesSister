# Import library yang diperlukan
import paho.mqtt.client as mqtt
import time
import random

# Alamat broker yang akan digunakan (gunakan broker publik dari Eclipse Project)
broker_address = "broker.hivemq.com"

# Buat client MQTT
client = mqtt.Client("Suhu1")

# Hubungkan client ke broker
client.connect(broker_address, port=1883)

client.loop_start()

# Publisher akan mengirim waktunya setiap 10 detik
while True:
    temperature = random.uniform(20.0, 30.0)
    print(f"Sensor 1, Suhu: {temperature}")

    # Menggunakan satu pesan dengan dua bagian (ID dan suhu)
    message = f"{temperature}"
    client.publish("info_sensor1", message, qos=1)
    time.sleep(5)

