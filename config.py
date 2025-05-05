"""
Team 2: Team Sprinkles
Abstract Document Storage Class
Document Storage Module
Kaleo Montero
Last edited --- 5/4/2025
"""
import os
import json

class config_handler():
    #this class creates and parses config files, ensuring they always contain all relevant fields

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
    
    def reset_config(self):
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
            self.reset_config()
            return self.fill_defaults(json.load(open(self.path, "r")))