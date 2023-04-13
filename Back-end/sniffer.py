import mysql.connector
from mysql.connector import errorcode
from scapy.all import *
from scapy.layers.http import HTTPRequest
import threading

words = ["password", "user", "username", "login", "pass", "Username", "Password", "User", "Email"]

# Create semaphore for database access
semaphore = threading.Semaphore()

def sniffed_packet(packet, interface, connection):
    if "IP" in packet: 
        if packet.haslayer(HTTPRequest):
            url = packet[HTTPRequest].Host + packet[HTTPRequest].Path
            ip_src=packet["IP"].src
            ip_dst=packet["IP"].dst
            print(ip_src, ip_dst, 'URL: ' + url.decode())
            add_data(connection, ip_src, ip_dst, url.decode(), '')
        if packet.haslayer(Raw):
            load = packet[Raw].load
            for i in words:
                if i in str(load):
                    print('Load: ' + load.decode())
                    ip_src=packet["IP"].src
                    ip_dst=packet["IP"].dst
                    add_data(connection, ip_src, ip_dst, '', load.decode())

def add_data(connection, ip_src, ip_dst, url, data):
    try:
        # Acquire semaphore to access database
        semaphore.acquire()
        cursor = connection.cursor()
        query = "INSERT INTO packets (ip_src, ip_dst, url, data) VALUES (%s, %s, %s, %s)"
        values = (ip_src, ip_dst, url, data)
        cursor.execute(query, values)
        connection.commit()
        print("Data added successfully")
    except mysql.connector.Error as error:
        print("Failed to add data to database: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
        # Release semaphore after finishing database access
        semaphore.release()

def main():
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='211228',
            database='sniffer2'
        )
        print("Connected to MySQL database")
        # Create 'packets' table if it doesn't exist
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS packets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_src VARCHAR(50),
                ip_dst VARCHAR(50),
                url VARCHAR(200),
                data TEXT
            )
        """)
        print("Table 'packets' created successfully")
        # Start sniffing packets
        interface = "Wi-Fi"
        sniff(iface=interface, store=False, prn=lambda x: sniffed_packet(x, interface, connection))
    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database: {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL connection closed")

main()
