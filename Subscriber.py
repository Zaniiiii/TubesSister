import paho.mqtt.client as mqtt
import time
import streamlit as st

data = []
data_sensor1 = []
data_sensor2 = []
data_sensor3 = []

def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')
    payload_numeric = float(payload_str)

    data.append({
        'topic': message.topic,
        'value':payload_numeric
    })

    print(message.topic + " = " + payload_str)

broker_address = "broker.hivemq.com"
client = mqtt.Client("subscriber")

# Hubungkan client ke broker
client.connect(broker_address, port=1883)

# Kaitkan fungsi callback
client.on_message = on_message

# Mulai loop client
client.loop_start()
st.header("Data yang diterima: ")

sub1 = st.subheader("Rata rata data yang diterima sensor")
table1 = st.table()
sub2 = st.subheader("Data sensor 1")
table2 = st.table()
sub3 = st.subheader("Data sensor 2")
table3 = st.table()
sub4 = st.subheader("Data sensor 3")
table4 = st.table()

# Subscriber akan menerima data dan menghitung rata-rata setiap 10 detik
try:
    while True:
        # Subscribe to topics
        client.subscribe("info_sensor1")
        client.subscribe("info_sensor2")
        client.subscribe("info_sensor3")
        time.sleep(5)
        if data:
            total_suhu = sum(data['value'] for data in data)
            hasil = total_suhu / len(data)
            print("Rata-rata Suhu Bandung saat ini:", hasil, "Celcius")
            print(" ")

            data_dengan_rata2 = data.copy()
            data_dengan_rata2.append({
                'topic':'Rata-rata Suhu Bandung saat ini',
                'value': hasil
            })
            sub1.empty()
            sub1 = st.subheader("Rata rata data yang diterima sensor")
            table1.empty()
            table1 = st.table(data_dengan_rata2)
            for x in data:
                if x["topic"] == "info_sensor1":
                    data_sensor1.append(x)
                elif x["topic"] == "info_sensor2":
                    data_sensor2.append(x)
                elif x["topic"] == "info_sensor3":
                    data_sensor3.append(x)

            sub2.empty()
            sub2 = st.subheader("Data sensor 1")
            table2.empty()
            table2 = st.table(data_sensor1)
            sub3.empty()
            sub3 = st.subheader("Data sensor 2")
            table3.empty()
            table3 = st.table(data_sensor2)
            sub4.empty()
            sub4 = st.subheader("Data sensor 3")
            table4.empty()
            table4 = st.table(data_sensor3)
            data = []

except KeyboardInterrupt:
    # Hentikan loop MQTT
    client.loop_stop()

