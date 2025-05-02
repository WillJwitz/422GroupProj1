from abstractServerComponent import abstract_server_component
from localServerComponent import local_server_component
from memoryServerComponent import memory_server_component
from mongoServerComponent import mongo_server_component, server_error
from interfaceComponent import app_window
from config import config_handler

def main():
    pdfs_path:str = "TestDummies"

    config_helper:config_handler = config_handler("config.txt");

    server:abstract_server_component = memory_server_component(pdfs_path)

    config_helper.add("allow_local", bool, True)
    config_helper.add("local_data_path", str, "Notes Data")
    config_helper.add("allow_server", bool, True)
    config_helper.add("server_ip", str, f"20.253.140.74:27017")
    config_helper.add("pdf_cache_path", str, ".pdfs")
    
    error: str = None
    config = config_helper.get_or_create()

    if config["allow_server"]:
        try:
            print(f"attemping mongo connection on ip: {config['server_ip']}")
            mongo_server = mongo_server_component(config["pdf_cache_path"], config["server_ip"])
            server = mongo_server

            #TODO: synchronize local data with server

            print("saving data on mongo server")
        except server_error as e:
            #Kaleo: not sure what to do for the error message here
            error = e.message

            #print error to console for debugging
            print(e.message)
            print(e.error)

            if(config["allow_local"]):
                #make error message for user less scary
                error = error + "\nRunning in local mode"
                
                print("saving data locally")
                server = local_server_component(pdfs_path, "Notes Data")
            else:
                error = "WARNING: no server connection, data will NOT be saved!"

    win = app_window(server, error)
    win.mainloop()

if __name__ == "__main__":
    main()
