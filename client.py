#!/usr/bin/env python3
import socket
import sys
import json


def main():
    filename = "sample_test.txt"
    server_address = "./uds_socket"
    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    print(f"Connecting to {server_address}")
    try:
        unix_socket.connect(server_address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    try:
        with open(filename) as file:
            message = file.read()
            unix_socket.sendall(bytes(message, 'utf-8'))

            response = unix_socket.recv(4096)
            print(response.decode('utf-8'))

    finally:
        unix_socket.close()


if __name__ == '__main__':
    main()
