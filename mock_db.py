from unittest import TestCase
import mysql.connector
from mysql.connector import errorcode
from unittest.mock import patch
import product


MYSQL_USER = "***REMOVED***"
MYSQL_PASSWORD = "***REMOVED***"
MYSQL_DB = "testdb"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"


class MockDB(TestCase):

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port = MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {}".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB

        query = """CREATE TABLE `lebensmittel` (
                  `Barcode` varchar(30) NOT NULL ,
                  `Lebensmittel` text NOT NULL,
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

        insert_data_query = """INSERT INTO `lebensmittel` (`Barcode`, `Lebensmittel`, `Anzahl`) VALUES
                            ('815', 'Testprodukt', 7),
                            ('200', 'Testprodukt_2', 1)"""
        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        cnx.close()

        testconfig ={
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(product.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)


        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()
        
