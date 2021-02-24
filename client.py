import socket
import sys
import json

def main():
    server_address = "./uds_socket"
    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    print(f"Connecting to {server_address}")
    try:
        unix_socket.connect(server_address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    try:
        request = {
                "id": "1",
                "type": "sign_transfer",
                "from_address": "0xc9fD61fA88B170275fA1de731950dcc45915e9dd",
                "to_address": "0xF9081018382ADb58e9C5781f9624f02e9Ee56Aac",
                "amount": "1"
        }
        message = json.dumps(request).encode('utf-8')
        unix_socket.sendall(message)

        data = unix_socket.recv(4096)
        response = json.loads(data)
        print(response)

    finally:
        unix_socket.close()

if __name__ == '__main__':
    main()
