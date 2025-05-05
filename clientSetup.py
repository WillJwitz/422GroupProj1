"""
Team 2: Team Sprinkles
Client setup script
Setup script (no module)
Kaleo Montero
Last edited --- 5/4/2025
"""
import argparse
from defaultConfigs import create_default_config

def main():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--server_ip', type=str, help='The mongo database\'s server ip')
    parser.add_argument('--pdf_cache_path', type=str, help='Temporary path for storing pdfs from the server')
    parser.add_argument('--allow_local', action='store_true', help='Allow files to be stored locally when app fails to connect to server')
    args = parser.parse_args()
    print(args.allow_local)
    create_default_config(server_ip=args.server_ip, pdf_cache_path=args.pdf_cache_path, allow_local=args.allow_local, reset=True)
    print("reset client config")

if __name__ == "__main__":
    main()