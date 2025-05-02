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