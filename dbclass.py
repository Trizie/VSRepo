import mysql.connector
from mysql.connector import errorcode
import sshtunnel

class DBclass:

    host = username = password = database = cnx = cur = None

    def __init__(self, host, username, password, database, ssh_user, ssh_pw):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.ssh_user = ssh_user
        self. ssh_pw = ssh_pw

    def insert_query(self, lebensmittelName, barcode, anzahl, kategorie):

        config = {
            'user': self.username,
            'password': self.password,
            'host': self.host,
            'database': self.database
            }

        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
                ("ssh.pythonanywhere.com"),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_pw,
                remote_bind_address=(
                        "Stutzenstein.mysql.pythonanywhere-services.com",
                        3306,
                ),
        ) as tunnel:
            self.cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                insert_query = """INSERT INTO lebensmittel
                                            (LebensmittelName, Barcode, Anzahl, Kategorie)
                                            VALUES (%s, %s, %s, %s)"""

                val = (lebensmittelName, barcode, anzahl, kategorie,)
                self.cur.execute(insert_query, val)
                self.cnx.commit()
                print(self.cur.rowcount, "Record inserted successfully")
                self.cur.close()
                print("Product added")
                return "True"
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(errorcode)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(errorcode)
                else:
                    print("insert query did not work")

    def select_query(self, barcode):

        config = {
            'user': self.username,
            'password': self.password,
            'host': self.host,
            'database': self.database
        }

        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
                ("ssh.pythonanywhere.com"),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_pw,
                remote_bind_address=(
                        "Stutzenstein.mysql.pythonanywhere-services.com",
                        3306,
                ),
        ) as tunnel:
            self.cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                sqlstatement = """SELECT Anzahl FROM lebensmittel WHERE Barcode=%s"""
                self.cur.execute(sqlstatement, (barcode,))
                value = self.cur.fetchall()
                return value
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(errorcode)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(errorcode)
                else:
                    print("sth didn't work")

    def delete_query(self, barcode):

        config = {
            'user': self.username,
            'password': self.password,
            'host': self.host,
            'database': self.database
            }

        sshtunnel.SSH_TIMEOUT = 10.0
        sshtunnel.TUNNEL_TIMEOUT = 10.0

        with sshtunnel.SSHTunnelForwarder(
                ("ssh.pythonanywhere.com"),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_pw,
                remote_bind_address=(
                        "Stutzenstein.mysql.pythonanywhere-services.com",
                        3306,
                ),
        ) as tunnel:
            self.cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                delete_query = """DELETE FROM lebensmittel WHERE Barcode=%s"""
                self.cur.execute(delete_query, (barcode,))
                self.cnx.commit()
                self.cur.close()
                print("Product deleted")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(errorcode)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(errorcode)
                else:
                    print("delete query didn't work")

    def disconnect(self):
        self.cnx.close()
        print()