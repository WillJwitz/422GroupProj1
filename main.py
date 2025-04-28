from abstractServerComponent import abstract_server_component
from localServerComponent import local_server_component
from memoryServerComponent import memory_server_component
from interfaceComponent import app_window
import json

#TODO: consider making a class for config
def load_config(path:str):
    try:
        json.load(open(path, "r"))
    except:
        return {}

def main():
    pdfs_path:str = "TestDummies"
    config_path:str = "config.txt"

    server:abstract_server_component = memory_server_component(pdfs_path)

    config:dict = load_config(config_path)
    if("allow_local" in config and config["allow_local"]):
        server = local_server_component(pdfs_path, "Notes Data")

    win = app_window(server, None)
    win.mainloop()


if __name__ == "__main__":
    main()