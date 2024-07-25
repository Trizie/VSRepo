import mysql.connector
from mysql.connector import errorcode
import sshtunnel

class DBclass:
    host = user = password = database = cnx = cur = None

    def __init__(self, host, user, password, database, ssh_user, ssh_pw):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.ssh_user = ssh_user
        self.ssh_pw = ssh_pw

    def insert_query(self, insert_query, *val):

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
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
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
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_pw,
                remote_bind_address=(
                        "Stutzenstein.mysql.pythonanywhere-services.com",
                        3306,
                ),
        ) as tunnel:
            self.cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=tunnel.local_bind_port,
            )
            try:
                self.cur = self.cnx.cursor()
                self.cur.execute(select_query, (val,))
                value = self.cur.fetchall()
                return value
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(errorcode)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(errorcode)
                else:
                    print("select query not successful")
            finally:
                self.cnx.close()


    def delete_query(self, barcode):

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
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
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
