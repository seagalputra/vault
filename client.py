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
        with open("sample_request.json") as file:
            message = json.load(file)
            request = json.dumps(message).encode('utf-8')
            unix_socket.sendall(request)
            data = unix_socket.recv(4096)

            response = json.loads(data)
            print(response)

    finally:
        unix_socket.close()

if __name__ == '__main__':
    main()
