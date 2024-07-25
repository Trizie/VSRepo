import random
import threading

import product
from paho.mqtt import client as mqtt_client

broker = "192.168.2.188"
port = 1883
topic = "arduino/barcode"
deleteTopic = "arduino/delete"
client_id = f"subscribe-{random.randint(0, 100)}"

product1 = product.Product(0, False, False, False, 1)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # (mqtt_client.Client(client_id))
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def processing_barcode(delMes):
    product1.barcodeStatus = False
    product1.deleteStatus = False
    productName = product1.get_productName()
    productCategory = product1.get_productCategory()

    if not product1.check_delete(delMes):
        print("Programm ist im Speichermodus")
        if product1.check_DB_contains_barcode() == "True":
            print("Produkt existiert schon")
            product1.raise_amount_of_product_in_DB()
        elif product1.check_DB_contains_barcode() == "False":
            print("Produkt ist neu")
            product1.add_product_to_DB(productName, productCategory)
            print("Produkt wurde zur Datenbank hinzugefügt.")
        else:
            print("Es gibt ein Problem mit dem Checken des Barcodes")
    else:
        print("Produkt wird gelöscht")
        product1.delete_product_from_DB()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            if msg.topic == "arduino/barcode":
                barcodeValue = str(msg.payload.decode("utf-8"))
                product1.barcode = barcodeValue.replace("\r", "")
                product1.barcodeStatus = True
            else:
                print("barcode not sent")

            if msg.topic == "arduino/delete":
                delMes = msg.payload.decode()
                print("delete status: " + delMes)
                product1.deleteStatus = True
            else:
                print("delete message not sent")
                product1.deleteStatus = False

            if product1.barcodeStatus is True and product1.deleteStatus is True:
                print(
                    "Barcodestatus und Löschstatus wurden übermittelt. Programm startet."
                )
                threading.Thread(
                    target=processing_barcode, daemon=True, args=(delMes,)
                ).start()
            else:
                print(
                    "Es sind nicht beide Statusmeldungen angekommmen. Programm kann nicht starten."
                )

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    client.subscribe(topic)
    client.subscribe(deleteTopic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
