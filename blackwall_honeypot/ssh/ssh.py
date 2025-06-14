#!/usr/bin/env python3
import socket, sys, threading
import _thread as thread
import paramiko

# generate keys with 'ssh-keygen -t rsa -f server.key'
HOST_KEY = paramiko.RSAKey(filename='server.key', password="123")
SSH_PORT = 2222
LOGFILE = 'logins.txt'  # File to log the user:password combinations to
LOGFILE_LOCK = threading.Lock()
last_remote_ip: str

class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            with open(LOGFILE, "a", encoding="utf-8") as logfile_handle:
                print(f"SSH::Login attempt::{last_remote_ip}::{username}:{password}")
                logfile_handle.write(username + ":" + password + "\n")
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'


def handle_connection(client):
    transport = paramiko.Transport(client)

    transport.add_server_key(HOST_KEY)

    if sys.platform in ['win32', 'win64']:
        transport.local_version = "SSH-2.0-OpenSSH_9.3p1 Microsoft-Windows_10.0.19044"
    else:
        transport.local_version = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"

    server_handler = SSHServerHandler()
    transport.start_server(server=server_handler)

    channel = transport.accept(1)
    if not channel is None:
        channel.close()
        print('Closing connection.')


def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SSH_PORT))
        server_socket.listen(100)
        print('SSH Honeypot Server Started.')

        paramiko.util.log_to_file('paramiko.log')

        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                print('Connection Received From:', client_addr)
                last_remote_ip = client_addr
                thread.start_new_thread(handle_connection, (client_socket,))
            except Exception as e:
                print("ERROR: Client handling")
                print(e)
    # Future: look for exceptions for 65 and 68
    except Exception as e:
        print("ERROR: Failed to create socket")
        print(e)
        sys.exit(1)


main()
