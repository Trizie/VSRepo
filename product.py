import json
import os

import dbclass
import requests
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
    "ssh_user": os.getenv("SSH_USER"),
    "ssh_pw": os.getenv("SSH_PASSWORD"),
}

connection = dbclass.DBclass(**config)


class Product:
    def __init__(self, barcode, delete, barcodeStatus, deleteStatus, amount):
        self.barcode = barcode
        self.delete = delete
        self.barcodeStatus = barcodeStatus
        self.deleteStatus = deleteStatus
        self.amount = amount

    def check_DB_contains_barcode(self):
        try:
            select_query = """SELECT * FROM lebensmittel WHERE Barcode=%s"""
            result = connection.select_query(select_query, self.barcode)
            if result == []:
                return "False"
            else:
                return "True"

        except Exception as exception:
            print(exception)
            print("Could not check if DB contains barcode.")

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
            return name

        except requests.HTTPError as exception:
            print(exception)
            return str(self.barcode)

        except Exception as exception:
            print(exception)
            return str(self.barcode)

    def get_amount_from_DB(self):
        try:
            select_query = """SELECT Anzahl FROM lebensmittel WHERE Barcode=%s"""
            result = connection.select_query(select_query, self.barcode)
            amount = result[0][0]
            number = int(amount)
            return number

        except Exception as exception:
            print(exception)

    def add_product_to_DB(self, product, category):
        try:
            insert_query = """INSERT INTO lebensmittel
                            (LebensmittelName, Barcode, Anzahl, Kategorie)
                            VALUES (%s, %s, %s, %s)"""

            val = product, self.barcode, self.amount, category
            connection.insert_query(insert_query, val)
            return "True"

        except Exception as exception:
            print(exception)

    def check_delete(self, msg):
        if msg == "true":
            delete = True
        else:
            delete = False
        return delete

    def delete_product_from_DB(self):
        try:
            amount = self.get_amount_from_DB()

            if amount == 1:
                connection.delete_query(self.barcode)
                print("Record deleted successfully")
                return "True"

            elif amount > 1:
                self.decrease_amount_of_product_in_DB()
                return "False"

            except Exception as exception:
                print(exception)

    def raise_amount_of_product_in_DB(self):
        try:
            amount = self.get_amount_from_DB() + 1
            update_query = """UPDATE lebensmittel SET Anzahl = %s WHERE Barcode = %s;"""
            val = amount, self.barcode
            connection.insert_query(update_query, val)
            return "True"

        except Exception as exception:
            print(exception)

    def decrease_amount_of_product_in_DB(self):
        try:
            amount = self.get_amount_from_DB() - 1
            update_query = """UPDATE lebensmittel SET Anzahl = %s WHERE Barcode = %s;"""
            val = amount, self.barcode
            connection.insert_query(update_query, val)
            return "True"

        except Exception as exception:
            print(exception)
