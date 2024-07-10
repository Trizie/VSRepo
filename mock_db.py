import os
from unittest import TestCase
from unittest.mock import patch

import mysql.connector
import product
import sshtunnel
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()

sshconfig = {
    "ssh_username": os.getenv("SSH_USER"),
    "ssh_password": os.getenv("SSH_PASSWORD"),
}
testconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "passwd": os.getenv("MYSQL_PASSWORD"),
    "db": os.getenv("MYSQL_DB_MOCK"),
}


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls):
        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "***REMOVED***.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **testconfig,
                port=tunnel.local_bind_port,
            )

            cursor = cnx.cursor(dictionary=True)

            query = """CREATE TABLE `lebensmittel` (
                      `Barcode` varchar(30) NOT NULL ,
                      `LebensmittelName` text NOT NULL,
                      `Anzahl` int NOT NULL
                    )"""
            try:
                cursor.execute(query)
                cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("test_table already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

            insert_data_query = """INSERT INTO `lebensmittel` (`Barcode`, `LebensmittelName`, `Anzahl`) VALUES
                                ('815', 'Testprodukt', 7),
                                ('200', 'Testprodukt_2', 1)"""
            try:
                cursor.execute(insert_data_query)
                cnx.commit()
            except mysql.connector.Error as err:
                print("Data insertion to test_table failed \n" + err)
            cursor.close()
            cnx.close()

            cls.mock_db_config = patch.dict(product.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        with sshtunnel.SSHTunnelForwarder(
            ("ssh.pythonanywhere.com"),
            **sshconfig,
            remote_bind_address=(
                "***REMOVED***.mysql.pythonanywhere-services.com",
                3306,
            ),
        ) as tunnel:
            cnx = mysql.connector.connect(
                **testconfig,
                port=tunnel.local_bind_port,
            )

            cursor = cnx.cursor(dictionary=True)

            try:
                cursor.execute("DROP TABLE 'lebensmittel'")
                cnx.commit()
                cursor.close()
            except mysql.connector.Error:
                print("Table does not exists. Dropping table failed")
            cnx.close()
