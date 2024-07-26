import random
import time

from paho.mqtt import client as mqtt_client

broker = "192.168.2.188"
port = 1883
topic = "arduino/barcode"
deleteTopic = "arduino/delete"
client_id = f"subscribe-{random.randint(0, 100)}"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg_delete = "false"
        result = client.publish(deleteTopic, msg_delete)
        msg_barcode = 4101530002505
        result_barcode = client.publish(topic, msg_barcode)
        status = result[0]
        status_barcode = result_barcode[0]
        if status == 0:
            print(f"Send `{msg_delete}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        if status_barcode == 0:
            print(f"Send `{msg_barcode}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 2:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == "__main__":
    run()
