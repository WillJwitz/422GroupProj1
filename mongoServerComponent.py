from abstractServerComponent import abstract_server_component
from pymongo import MongoClient
import gridfs
import os

#Kaleo: pdfs path and server ip are now in config
#but these seeemed fine as constants
DB_NAME = "project_database"
NOTE_COLLECTION = "user_notes"

class server_error(Exception):
    def __init__(self, message: str, inner_error: BaseException = None): 
        self.message: str = message
        self.error: BaseException = inner_error

    def get_inner(self) -> BaseException:
        return self.error


class mongo_server_component(abstract_server_component):
    def __init__(self, pdf_cache_path: str, server_ip: str):
        #Kaleo: reduce timeout to make startup less slow
        timeout = 4000 
        self.client = MongoClient(f"mongodb://{server_ip}", serverSelectionTimeoutMS = timeout)
        self.db = self.client[DB_NAME]
        self.fs = gridfs.GridFS(self.db)
        self.pdfs_path:str = pdf_cache_path
        self.user:str|None = None

        #Kaleo: basic error handling
        try:
             self.client.server_info()
        except Exception as e:
            raise server_error("Failed to connect to server", e)


    def authenticate(self, username: str) -> bool:
        #drew? any input on the authentication process? (we gotta be secure)
        #TODO: do we check with server if the username is valid?
        self.user = username
        return True

    def get_pdfs(self) -> list[str]:
        return [f.filename for f in self.fs.find()]

    def get_pdf_path(self, filename: str) -> str:
        local_path = os.path.join(self.pdfs_path, filename)
        if not os.path.isfile(local_path):
            grid_out = self.fs.find_one({"filename": filename})
            if grid_out:
                if not os.path.exists(self.pdfs_path):
                    os.makedirs(self.pdfs_path)
                with open(local_path, 'wb') as f:
                    f.write(grid_out.read())
        return local_path

    def get_notes(self, pdfName: str) -> list[str]:
        notes = self.db[NOTE_COLLECTION].find({"pdfName": pdfName, "username": self.user})
        return [note["noteName"] for note in notes]

    def get_note_file(self, pdfName: str, noteName: str) -> dict:
        note = self.db[NOTE_COLLECTION].find_one({"pdfName": pdfName, "noteName": noteName, "username": self.user})
        return note if note else {}

    def send_note(self, pdfName: str, noteName: str, jsonNote: dict) -> bool:
        self.db[NOTE_COLLECTION].update_one(
            {"pdfName": pdfName, "noteName": noteName, "username": self.user},
            {"$set": jsonNote},
            upsert=True
        )
        return True
    
    def close(self):
        self.client.close()
