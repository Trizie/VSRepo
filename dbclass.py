import mysql.connector
from mysql.connector import errorcode
import sshtunnel
import os
from dotenv import load_dotenv

load_dotenv()

sshconfig = {
    "ssh_username": os.getenv("SSH_USER"),
    "ssh_password": os.getenv("SSH_PASSWORD"),
}

config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
}

class DBclass:

    def insert_query(self, insert_query, *val):

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
            self.cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                self.cur.execute(insert_query, *val)
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
            finally:
                self.cnx.close()

    def select_query(self, select_query, val):

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
            self.cnx = mysql.connector.connect(
                **config,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                self.cur.execute(select_query, (val,))
                value = self.cur.fetchall()
                print(value)
                return value
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(errorcode)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(errorcode)
                else:
                    print("sth didn't work")
            finally:
                self.cnx.close()


    def delete_query(self, barcode):

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
            finally:
                self.cnx.close()

    def disconnect(self):
        pass