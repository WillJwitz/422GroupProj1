import argparse
from mongoServerComponent import mongo_server_component, server_error
from localServerComponent import local_server_component

def getUsers():
    #TODO make this and the interface use the same function
    return ["Student1", "Student2", "Student3"]

def main():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('server_ip', type=str, help='The mongo database\'s server ip')
    args = parser.parse_args()

    try:
        mongo_server = mongo_server_component(".setup_pdf_cache", args.server_ip)
        local_server = local_server_component("setup/pdfs", "setup/notes")
        for u in getUsers():
            local_server.authenticate(u);
            mongo_server.authenticate(u);
            for p in local_server.get_pdfs():
                for n in local_server.get_notes():
                    data = local_server.get_note_file(p,n)
                    mongo_server.send_note(p,n, data)
        print("server setup complete!")
    except server_error as e:
        print(e.message)

if __name__ == "__main__":
    main()