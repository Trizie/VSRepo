import json
import os

import mysql.connector
import requests
import sshtunnel
from dotenv import load_dotenv

load_dotenv()

sshconfig = {
    "ssh_username": os.getenv("SSH_USER"),
    "ssh_password": os.getenv("SSH_PASSWORD"),
}
config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "passwd": os.getenv("MYSQL_PASSWORD"),
    "db": os.getenv("MYSQL_DB"),
}


class Product:
    def __init__(self, barcode, delete, barcodeStatus, deleteStatus, amount):
        self.barcode = barcode
        self.delete = delete
        self.barcodeStatus = barcodeStatus
        self.deleteStatus = deleteStatus
        self.amount = amount

    def check_DB_contains_barcode(self):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            connection = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                cur = connection.cursor()
                sql = "SELECT Barcode FROM lebensmittel WHERE Barcode=%s"

                cur.execute(sql, (self.barcode,))
                result = cur.fetchall()
                print(result)
                row_count = cur.rowcount
                print("barcode checked function")
                if row_count == 0:
                    return "False"
                else:
                    return "True"

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                cur.close()
                connection.close()
                print("DB connection is closed")

    def get_productCategory(self):
        try:
            url = "https://world.openfoodfacts.org/api/2/product/"
            urlBarcode = url + self.barcode
            product = requests.get(urlBarcode)
            data = json.loads(product.text)
            category = data["product"]["categories"]
            return category

        except requests.HTTPError as exception:
            print(exception)
            return "no category available"

        except Exception as exception:
            print(exception)
            return "no category available"

    def get_productName(self):
        try:
            url = "https://world.openfoodfacts.org/api/2/product/"
            urlBarcode = url + self.barcode
            product = requests.get(urlBarcode)
            data = json.loads(product.text)
            name = data["product"]["product_name"]
            print(name)
            return name

        except requests.HTTPError as exception:
            print(exception)
            return str(self.barcode)

        except Exception as exception:
            print(exception)
            return str(self.barcode)

    def get_amount_from_DB(self):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            connection = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                cur = connection.cursor()
                get_query = "SELECT Anzahl FROM lebensmittel WHERE Barcode=%s"

                cur.execute(get_query, (self.barcode,))
                value = cur.fetchall()
                print(value)
                print(type(value))
                amount = value[0][0]
                print(amount)
                number = int(amount)
                cur.close()
                return number

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                connection.close()
                print("DB connection is closed")

    def add_product_to_DB(self, product, category):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                cur = cnx.cursor()
                insert_query = """INSERT INTO lebensmittel
                                (LebensmittelName, Barcode, Anzahl, Kategorie)
                                VALUES (%s, %s, %s, %s)"""

                val = product, self.barcode, self.amount, category
                print(self.barcode)
                cur.execute(insert_query, val)
                cnx.commit()
                print(cur.rowcount, "Record inserted successfully")
                cur.close()
                print("Product added")
                return "True"

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                cnx.close()
                print("DB connection is closed")

    def check_delete(self, msg):
        if msg == "true":
            delete = True
        else:
            delete = False
            print("nicht löschen")
        return delete

    def delete_product_from_DB(self):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                cur = cnx.cursor()
                amount = self.get_amount_from_DB()

                if amount == 1:
                    delete_query = """DELETE FROM lebensmittel WHERE Barcode = %s"""
                    cur.execute(delete_query, (self.barcode,))
                    cnx.commit()
                    print(cur.rowcount, "Record deleted successfully")
                    cur.close()
                    return "True"

                elif amount > 1:
                    self.decrease_amount_of_product_in_DB()
                    return "False"

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                cnx.close()
                print("DB connection is closed")

    def raise_amount_of_product_in_DB(self):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                amount = self.get_amount_from_DB() + 1
                cur = cnx.cursor()

                update_query = (
                    """UPDATE lebensmittel SET Anzahl = %s WHERE Barcode = %s;"""
                )
                val = amount, self.barcode
                cur.execute(update_query, val)
                cnx.commit()
                print(cur.rowcount, "Record updated successfully")
                cur.close()
                return "True"

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                cnx.close()
                print("DB connection is closed")

    def decrease_amount_of_product_in_DB(self):
        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "Stutzenstein.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                amount = self.get_amount_from_DB() - 1
                cur = cnx.cursor()

                update_query = (
                    """UPDATE lebensmittel SET Anzahl = %s WHERE Barcode = %s;"""
                )
                val = amount, self.barcode
                cur.execute(update_query, val)
                cnx.commit()
                print(cur.rowcount, "Record updated successfully")
                cur.close()
                return "True"

            except mysql.connector.Error as err:
                print(err.msg)

            finally:
                cnx.close()
                print("DB connection is closed")
