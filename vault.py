#!/usr/bin/env python3
import socket
import os
import argparse
import yaml
import json

from web3 import Web3

def create_transaction(transaction_request):
    w3 = Web3(Web3.HTTPProvider(os.environ['NODE_URL']))
    id = transaction_request['id']
    nonce = w3.eth.getTransactionCount(transaction_request['from_address'])
    to_address = transaction_request['to_address']
    amount = w3.toWei(int(transaction_request['amount']), 'ether')
    gas_price = w3.toWei('50', 'gwei')
    gas = 2000000

    transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': amount,
            'gas': gas,
            'gasPrice': gas_price
    }

    signed_transaction = w3.eth.account.signTransaction(transaction, os.environ['PRIVATE_KEY'])
    transaction_hash = w3.toHex(signed_transaction.hash)
    return { 'id': id, 'tx': transaction_hash }

def configure_server(server_address):
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

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
                    response = create_transaction(request)
                    byte_response = json.dumps(response).encode('utf-8')
                    connection.sendall(byte_response)

def load_config():
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            for key, value in config.items():
                os.environ[key.upper()] = value

        except yaml.YAMLError as exception:
            print(exception)

def start_server():
    parser = argparse.ArgumentParser(description="Vault application")
    parser.add_argument("path", metavar="path", type=str, help="Initial UNIX socket path")

    args = parser.parse_args()

    socket_path = args.path

    load_config()
    configure_server(socket_path)

if __name__ == '__main__':
    start_server()
