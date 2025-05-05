"""
Team 2: Team Sprinkles
Mongo Document Storage Class
Document Storage Module
Sawyer Christenssen, Drew Christie, Kaleo Montero
Last edited --- 5/4/2025
"""
from abstractServerComponent import abstract_server_component
from pymongo import MongoClient
import gridfs
import os

DB_NAME = "project_database"
NOTE_COLLECTION = "user_notes"

class server_error(Exception):
    def __init__(self, message: str, inner_error: BaseException = None): 
        self.message: str = message
        self.error: BaseException = inner_error

    def get_inner(self) -> BaseException:
        return self.error


class mongo_server_component(abstract_server_component):
    #A server component implementation that uses a mongo server to store notes
    #Designed for the main online mode of use

    def __init__(self, pdf_cache_path: str, server_ip: str):
        #timout is lower than default to make app launch faster
        timeout = 4000 
        self.client = MongoClient(f"mongodb://{server_ip}", serverSelectionTimeoutMS = timeout)
        self.db = self.client[DB_NAME]
        self.fs = gridfs.GridFS(self.db)
        self.pdfs_path:str = pdf_cache_path
        self.user:str|None = None

        #check if connection is valid, throw a server error if not
        try:
             self.client.server_info()
        except Exception as e:
            raise server_error("Failed to connect to server", e)


    def authenticate(self, username: str) -> bool:
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

    #extra function added to allow uploading files during server setup
    #in the future this might be added to the abstract component, to allow for synching
    def send_pdf(self, pdfName:str, pdfPath: str) -> bool:
        with open(pdfPath, 'rb') as f:
            hadOld = False
            for file in self.fs.find({"filename": pdfName}):
                self.fs.delete(file._id)
                hadOld = True
            self.fs.put(f.read(), filename = pdfName)
            if(hadOld):
                print("uploaded updated pdf")
            else:
                print("uploaded new pdf")
        return True
    
    def delete_all_pdfs(self):
        for file in self.fs.find():
            self.fs.delete(file._id)
    
    def close(self):
        self.client.close()
