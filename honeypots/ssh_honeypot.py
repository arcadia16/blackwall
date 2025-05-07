import sys

import paramiko
import socket
import threading
from datetime import datetime
from flask import Flask, jsonify
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
ssh_logs = []

# Generate persistent host key (RSA 2048)
HOST_KEY_PATH = '../ssh_host_key'
if not os.path.exists(HOST_KEY_PATH):
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(HOST_KEY_PATH)
host_key = paramiko.RSAKey(filename=HOST_KEY_PATH)


class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()
        self.session_id = os.urandom(16).hex()
        self.client_version = None

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'client_ip': self.client_ip,
            'username': username,
            'password': password,
            'client_version': self.client_version,
            'session_id': self.session_id
        }
        ssh_logs.append(log_entry)
        logging.info(f"SSH attempt: {log_entry}")
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED


def handle_ssh_connection(client_sock):
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(host_key)
    if sys.platform in ['win32', 'win64']:
        transport.local_version = "SSH-2.0-OpenSSH_9.3p1 Microsoft-Windows_10.0.19044"
    else:
        transport.local_version = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"

    try:
        transport.start_server(server=SSHServer(client_sock.getpeername()[0]))
        channel = transport.accept(20)
        if channel:
            channel.close()
    except paramiko.SSHException:
        pass
    finally:
        transport.close()


def ssh_honeypot():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', 22))
    server_sock.listen(100)

    logging.info("SSH honeypot listening on port 22")
    while True:
        client_sock, addr = server_sock.accept()
        logging.info(f"Connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_ssh_connection, args=(client_sock,)).start()


@app.route('/logs')
def get_logs():
    return jsonify({'ssh_attempts': ssh_logs})


if __name__ == '__main__':
    # Start SSH honeypot in background
    ssh_thread = threading.Thread(target=ssh_honeypot, daemon=True)
    ssh_thread.start()

    # Start Flask web interface
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)