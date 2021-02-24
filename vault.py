#!/usr/bin/env python3
import argparse
import os
import yaml
import json
import socket

from web3 import Web3

class Transaction:
    def __init__(self, node_url, private_key):
        self.node_url = node_url
        self.private_key = private_key

    def create_transaction(self, transaction_request):
        w3 = Web3(Web3.HTTPProvider(self.node_url))
        id = transaction_request['id']
        nonce = w3.eth.getTransactionCount(transaction_request['from_address'])
        to_address = transaction_request['to_address']
        amount = w3.toWei(float(transaction_request['amount']), 'ether')
        gas_price = w3.toWei('147', 'gwei')
        gas = 21000

        transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': amount,
                'gas': gas,
                'gasPrice': gas_price
        }

        signed_transaction = w3.eth.account.signTransaction(transaction, self.private_key)
        transaction_hash = w3.toHex(signed_transaction.rawTransaction)
        return { 'id': id, 'tx': transaction_hash }

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
                    transaction = Transaction(os.environ['NODE_URL'], os.environ['PRIVATE_KEY'])
                    signed_transaction = transaction.create_transaction(request)
                    byte_response = json.dumps(signed_transaction).encode('utf-8')
                    connection.sendall(byte_response)

def main():
    parser = argparse.ArgumentParser(description="Vault Application")
    parser.add_argument("path", metavar="path", type=str, help="Initial UNIX socket path")

    args = parser.parse_args()

    server_address = args.path

    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = f"{root_dir}/config.yml"
    load_config(config_path)
    configure_server(server_address)

if __name__ == '__main__':
    main()
