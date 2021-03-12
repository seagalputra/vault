#!/usr/bin/env python3
import argparse
import os
import yaml
import json
import socket

from web3 import Web3


class Transaction:
    def __init__(self, node_url, private_keys):
        self.node_url = node_url
        self.private_keys = private_keys

    def create_transaction(self, transaction_request):
        w3 = Web3(Web3.HTTPProvider(self.node_url))
        id = transaction_request['id']
        from_address = transaction_request['from_address']
        to_address = transaction_request['to_address']
        amount = transaction_request['amount']

        nonce = w3.eth.getTransactionCount(from_address)
        amount = w3.toWei(float(amount), 'ether')
        gas_price = w3.toWei('147', 'gwei')
        gas = 21000

        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': amount,
            'gas': gas,
            'gasPrice': gas_price
        }
        filtered_key = list(filter(lambda key: key['address'] ==
                                   from_address, self.private_keys))
        private_key = filtered_key[0]['private_key']

        signed_transaction = w3.eth.account.signTransaction(
            transaction, private_key)
        transaction_hash = w3.toHex(signed_transaction.rawTransaction)
        return {'id': id, 'tx': transaction_hash}


def load_config(path):
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)

            return config
        except yaml.YAMLError as exception:
            print(exception)


def unlink_socket(address):
    try:
        os.unlink(address)
    except OSError:
        if os.path.exists(address):
            raise


def parse_message(messages):
    return [message for message in messages.split("\n")]


def configure_server(server_address):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = f"{root_dir}/config.yml"
    config = load_config(config_path)

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

                    transaction = Transaction(
                        config['node_url'], config['private_keys'])
                    messages = parse_message(data.decode('utf-8'))
                    response = []
                    for message in messages:
                        request = json.loads(message)
                        signed_transaction = transaction.create_transaction(
                            request)
                        response.append(json.dumps(
                            signed_transaction))

                    byte_response = '\n'.join(response).encode('utf-8')
                    connection.sendall(byte_response)


def main():
    parser = argparse.ArgumentParser(description="Vault Application")
    parser.add_argument("path", metavar="path", type=str,
                        help="Initial UNIX socket path")

    args = parser.parse_args()

    server_address = args.path

    configure_server(server_address)


if __name__ == '__main__':
    main()
