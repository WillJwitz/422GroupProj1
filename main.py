from abstractServerComponent import abstract_server_component
from localServerComponent import local_server_component
from memoryServerComponent import memory_server_component
from mongoServerComponent import mongo_server_component, server_error
from interfaceComponent import app_window
from defaultConfigs import create_default_config

def main():
    pdfs_path:str = "TestDummies"

    server:abstract_server_component = memory_server_component(pdfs_path)
    error: str = None

    #TODO: do we want missing configs to be a fatal error instead?
    config = create_default_config()

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
