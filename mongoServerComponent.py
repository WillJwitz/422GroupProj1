from abstractServerComponent import abstract_server_component
from pymongo import MongoClient
import gridfs
import os

MONGO_IP = "20.253.140.74:27017" #rewrite this once we have a config file
DB_NAME = "project_database"
NOTE_COLLECTION = "user_notes"
PDF_DIR = "./pdfs" #where local pdfs are stored (can be changed)

class mongo_server_component(abstract_server_component):
    def __init__(self):
        self.client = MongoClient(f"mongodb://{MONGO_IP}")
        self.db = self.client[DB_NAME]
        self.fs = gridfs.GridFS(self.db)

    def authenticate(self, username: str) -> bool:
        #drew? any input on the authentication process? (we gotta be secure)
        return True

    def get_pdfs(self) -> list[str]:
        return [f.filename for f in self.fs.find()]

    def get_pdf_path(self, filename: str) -> str:
        local_path = os.path.join(PDF_DIR, filename)
        if not os.path.isfile(local_path):
            grid_out = self.fs.find_one({"filename": filename})
            if grid_out:
                if not os.path.exists(PDF_DIR):
                    os.makedirs(PDF_DIR)
                with open(local_path, 'wb') as f:
                    f.write(grid_out.read())
        return local_path

    def get_notes(self, pdfName: str) -> list[str]:
        notes = self.db[NOTE_COLLECTION].find({"pdfName": pdfName})
        return [note["noteName"] for note in notes]

    def get_note_file(self, pdfName: str, noteName: str) -> dict:
        note = self.db[NOTE_COLLECTION].find_one({"pdfName": pdfName, "noteName": noteName})
        return note if note else {}

    def send_note(self, pdfName: str, noteName: str, jsonNote: dict) -> bool:
        self.db[NOTE_COLLECTION].update_one(
            {"pdfName": pdfName, "noteName": noteName},
            {"$set": jsonNote},
            upsert=True
        )
        return True
    
    def close(self):
        self.client.close()
