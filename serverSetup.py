"""
Team 2: Team Sprinkles
Client setup script
Setup script (no module)
Kaleo Montero
Last edited --- 5/4/2025
"""
import argparse
from mongoDocumentStorage import mongo_document_storage, server_error
from localDocumentStorage import local_document_storage

def getUsers():
    #TODO make this and the interface use the same function
    return ["Student1", "Student2", "Student3"]

def main():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('server_ip', type=str, help='The mongo database\'s server ip')
    parser.add_argument('--clear_pdfs', action='store_true', help='Deletes pdfs already on the server')
    args = parser.parse_args()

    try:
        #connect to both remote mongo server AND local setup filesystem
        #to transfer data from local to remote
        mongo_server = mongo_document_storage(".setup_pdf_cache", args.server_ip)
        local_server = local_document_storage("Setup/pdfs", "Setup/notes")

        if(args.clear_pdfs):
            mongo_server.delete_all_pdfs()
            print("deleted pdfs on server")
        
        #start by uploading pdfs
        #this shouldn't need user authentication
        for p in local_server.get_pdfs():
                mongo_server.send_pdf(p, local_server.get_pdf_path(p))
        
        #upload user data, which is just notes
        for u in getUsers():
            local_server.authenticate(u);
            mongo_server.authenticate(u);
            for p in local_server.get_pdfs():
                for n in local_server.get_notes(p):
                    data = local_server.get_note_file(p,n)
                    print(data["header"])
                #    mongo_server.send_note(p,n, data)
        print("server setup complete!")
    except server_error as e:
        print(e.message)

if __name__ == "__main__":
    main()