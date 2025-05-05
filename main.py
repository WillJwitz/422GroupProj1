"""
Team 2: Team Sprinkles
Main function
Entrypoint Module
Hayden Houlihan, Kaleo Montero
Last edited --- 5/4/2025
"""

from abstractDocumentStorage import abstract_document_storage
from localDocumentStorage import local_document_storage
from memoryDocumentStorage import memory_document_storage
from mongoDocumentStorage import mongo_document_storage, server_error
from interfaceComponent import app_window
from defaultConfigs import create_default_config

def main():
    #local pdfs path
    pdfs_path:str = "TestDummies"

    server:abstract_document_storage = memory_document_storage(pdfs_path)
    error: str = None

    config = create_default_config()

    if config["allow_server"]:
        try:
            print(f"attemping mongo connection on ip: {config['server_ip']}")
            mongo_server = mongo_document_storage(config["pdf_cache_path"], config["server_ip"])
            server = mongo_server
            print(len(server.get_pdfs()))
            #TODO: synchronize local data with server

            print("saving data on mongo server")
        except server_error as e:
            error = e.message

            #print error to console for debugging
            print(e.message)
            print(e.error)

            if(config["allow_local"]):
                #make error message for user less scary
                error = error + "\nRunning in local mode"
                
                print("saving data locally")
                server = local_document_storage(pdfs_path, "Notes Data")
            else:
                #make error message for user more scary
                error = "WARNING: no server connection, data will NOT be saved!"

    #launch app with the chosen server, and notify user of error if present
    win = app_window(server, error)
    win.mainloop()

if __name__ == "__main__":
    main()
