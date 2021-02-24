import os

from web3 import Web3

class Transaction:
    def __init__(self):
        self.node_url = os.environ['NODE_URL']
        self.private_key = os.environ['PRIVATE_KEY']

    def create_transaction(self, transaction_request):
        w3 = Web3(Web3.HTTPProvider(self.node_url))
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

        signed_transaction = w3.eth.account.signTransaction(transaction, self.private_key)
        transaction_hash = w3.toHex(signed_transaction.hash)
        return { 'id': id, 'tx': transaction_hash }
