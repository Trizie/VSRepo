import random

import product
from paho.mqtt import client as mqtt_client

broker = "192.168.2.31"
port = 1883
topic = "arduino/barcode"
deleteTopic = "arduino/delete"
client_id = f"subscribe-{random.randint(0, 100)}"

product = product.Product(0, False, False, False, 1)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # (mqtt_client.Client(client_id))
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            if msg.topic == "arduino/barcode":
                barcodeValue = str(msg.payload.decode("utf-8"))
                product.barcode = barcodeValue.replace("\r", "")
                print(product.barcode)
                product.barcodeStatus = True
            else:
                print("barcode not sent")

            if msg.topic == "arduino/delete":
                delMes = msg.payload.decode()
                print("delete status: " + delMes)
                product.deleteStatus = True
            else:
                print("delete message not sent")
                product.deleteStatus = False

            if (product.barcodeStatus == True and product.deleteStatus == True):
                print(
                    "Beide Statusmeldungen (Barcodestatus und Löschstatus) sind angekommen."
                )
                product.barcodeStatus = False
                product.deleteStatus = False
                productName = product.get_productName()

                if not product.check_delete(delMes):
                    print("Programm ist im Speichermodus")
                    if product.check_DB_contains_barcode() == "True":
                        print("Produkt existiert schon")
                        product.raise_amount_of_product_in_DB()
                    elif product.check_DB_contains_barcode() == "False":
                        print("Produkt ist neu")
                        product.add_product_to_DB(productName)
                    else:
                        print("Es gibt ein Problem mit dem Checken des Barcodes")
                else:
                    print("Produkt wird gelöscht")
                    product.delete_product_from_DB()

            else:
                print(
                    "Es sind nicht beide Statusmeldungen (Barcodestatus und Löschstatus) angekommmen"
                )

        except:
            print("on_message error")

    client.subscribe(topic)
    client.subscribe(deleteTopic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
