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
        default = {}
        for k in self.cfgs:
            default[k] = self.cfgs[k][1]
        json.dump(default, open(self.path, "w"), indent=4)
    
    def get_or_create(self):
        if(os.path.isfile(self.path)):
            try:
                return self.fill_defaults(json.load(open(self.path, "r")))
            except:
                default = {}
                for k in self.cfgs:
                    default[k] = self.cfgs[k][1]
                return default
        else:
            self.create_config()
            return self.fill_defaults(json.load(open(self.path, "r")))

def main():
    pdfs_path:str = "TestDummies"

    config_helper:config_handler = config_handler("config.txt");

    server:abstract_server_component = memory_server_component(pdfs_path)

    config_helper.add("allow_local", bool, True)

    config = config_helper.get_or_create()

    if(config["allow_local"]):
        server = local_server_component(pdfs_path, "Notes Data")

    win = app_window(server, None)
    win.mainloop()


if __name__ == "__main__":
    main()