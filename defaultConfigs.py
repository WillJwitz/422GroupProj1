"""
Team 2: Team Sprinkles
Default Configuration Setup
Entrypoint Module
Kaleo Montero
Last edited --- 5/3/2025
"""
from config import config_handler
from typing import Any

def default_server_ip() -> str:
    return f"20.253.140.74:27017"

def default_pdf_cache_path() -> str:
    return ".pdfs"


def create_default_config(server_ip:str = None, pdf_cache_path = None, allow_local = True, reset = False) -> dict[str, Any]:
    if server_ip == None:
        server_ip = default_server_ip()
    if pdf_cache_path == None:
        pdf_cache_path = default_pdf_cache_path()
    
    config_helper:config_handler = config_handler("config.txt");

    config_helper.add("allow_local", bool, allow_local)
    config_helper.add("local_data_path", str, "Notes Data")
    config_helper.add("allow_server", bool, True)
    config_helper.add("server_ip", str, server_ip)
    config_helper.add("pdf_cache_path", str, pdf_cache_path)
    if reset:
        config_helper.reset_config()
    
    return config_helper.get_or_create()