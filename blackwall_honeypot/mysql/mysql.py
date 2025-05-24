import socket
from socket import socket as SocketClass, error as SocketError
import threading
import logging
from datetime import datetime
import sys

from handshake_parser import parse_and_print


LISTEN_PORT = 3306
MYSQL_CONTAINER_IP = '127.0.0.1'
MYSQL_CONTAINER_PORT = 3307
LOG_FILE = 'mysql_honeypot.log'


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


def log_connection(client_ip, status):
    entry = f"{datetime.now().isoformat()} - {client_ip} - {status}"
    logging.info(entry)


def handle_client(client_sock):
    client_ip = client_sock.getpeername()[0]
    log_connection(client_ip, "CONNECTED")

    try:
        # Connect to real MySQL container
        mysql_sock = SocketClass(socket.AF_INET, socket.SOCK_STREAM)
        mysql_sock.connect((MYSQL_CONTAINER_IP, MYSQL_CONTAINER_PORT))

        # Start forwarding
        threading.Thread(target=forward, args=(client_sock, mysql_sock)).start()
        threading.Thread(target=forward, args=(mysql_sock, client_sock)).start()

    except Exception as e:
        log_connection(client_ip, f"ERROR: {str(e)}")
        client_sock.close()


def forward(source: SocketClass, destination: SocketClass):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            print("received data!")
            parse_and_print(data)
            destination.sendall(data)
    except SocketError:
        pass
    finally:
        source.close()
        destination.close()


def start_proxy():
    try:
        server = SocketClass(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', LISTEN_PORT))
        server.listen(100)

        logging.info(f"Honeypot running on port {LISTEN_PORT}")
        logging.info(f"Forwarding to {MYSQL_CONTAINER_IP}:{MYSQL_CONTAINER_PORT}")

        while True:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock,)).start()

    except PermissionError:
        logging.error("Error: Need sudo to bind to port 3306")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    start_proxy()
