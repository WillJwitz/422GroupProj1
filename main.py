from abstractServerComponent import abstract_server_component
from localServerComponent import local_server_component
from memoryServerComponent import memory_server_component
from interfaceComponent import app_window
import os
import json

class config_handler():
    def __init__(self, path:str):
        self.path:str = path
        self.cfgs = {}
    
    def add(self, key:str, t:type, v):
        self.cfgs[key] = (t, v)

    def fill_defaults(self, data):
        for k in self.cfgs:
            if not k in data:
                data[k] = self.cfgs[k][1]
        return data
    
    def create_config(self):
        default = self.fill_defaults({})
        json.dump(default, open(self.path, "w"), indent=4)
    
    def get_or_create(self):
        if(os.path.isfile(self.path)):
            try:
                data = json.load(open(self.path, "r"))
                data = self.fill_defaults(data)
                json.dump(data, open(self.path, "w"), indent=4)
                return data
            except:
                default = self.fill_defaults({})
                return default
        else:
            self.create_config()
            return self.fill_defaults(json.load(open(self.path, "r")))

def main():
    pdfs_path:str = "TestDummies"

    config_helper:config_handler = config_handler("config.txt");

    server:abstract_server_component = memory_server_component(pdfs_path)

    config_helper.add("allow_local", bool, True)
    config_helper.add("server_ip", str, f"20.253.140.74:27017")

    config = config_helper.get_or_create()

    print("server ip: ")
    print(config["server_ip"])
    print("WARNING: servers not implemented yet!")

    if(config["allow_local"]):
        print("saving data locally")
        server = local_server_component(pdfs_path, "Notes Data")

    win = app_window(server, None)
    win.mainloop()


if __name__ == "__main__":
    main()