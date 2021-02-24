import argparse
import os
from .server import load_config, configure_server

def main():
    parser = argparse.ArgumentParser(description="Vault Application")
    parser.add_argument("path", metavar="path", type=str, help="Initial UNIX socket path")

    args = parser.parse_args()

    server_address = args.path

    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = f"{root_dir}/../config.yml"
    load_config(config_path)
    configure_server(server_address)

if __name__ == '__main__':
    main()
