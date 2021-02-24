import os
import yaml
import json
import socket
from transaction import Transaction

def load_config(path):
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)

            for key, value in config.items():
                os.environ[key.upper()] = value
        except yaml.YAMLError as exception:
            print(exception)

def unlink_socket(address):
    try:
        os.unlink(address)
    except OSError:
        if os.path.exists(address):
            raise

def configure_server(server_address):
    unlink_socket(server_address)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as unix_socket:
        print(f"Starting server in address {server_address}")
        unix_socket.bind(server_address)
        unix_socket.listen(1)

        while True:
            connection, _ = unix_socket.accept()
            with connection:
                while True:
                    data = connection.recv(4096)

                    if not data:
                        break

                    request = json.loads(data)
                    transaction = Transaction()
                    signed_transaction = transaction.create_transaction(request)
                    byte_response = json.dumps(signed_transaction).encode('utf-8')
                    connection.sendall(byte_response)
