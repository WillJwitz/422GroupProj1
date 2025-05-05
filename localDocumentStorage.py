"""
Team 2: Team Sprinkles
Local Document Storage Class
Document Storage Module
Kaleo Montero
Last edited --- 5/4/2025
"""
from abstractDocumentStorage import abstract_document_storage
import os
import json
from typing import Any

class local_document_storage(abstract_document_storage):
    #A server component implementation that uses local files to store notes
    #Designed for use in offline mode

    def __init__(self, pdfs_path: str, storage_path:str ):
        super().__init__()
        self.data:dict = {}

        self.storage_path:str = storage_path
        self.pdfs_path:str = pdfs_path

        try:
            os.mkdir(self.storage_path)
        except:
            pass

        # Filtering only the files.
        files = [file for file in os.listdir(self.pdfs_path) if os.path.isfile(self.pdfs_path+'/'+file)]

        self.pdfs:dict[str, str] = {}

        for file in files:
            name = os.path.splitext(file)[0]
            self.pdfs[name] = self.pdfs_path+'/'+file
        
        self.selected:str = ""

    def user_path(self):
        return self.storage_path + "/" + self.selected
    
    def notes_path(self, pdf:str):
        return self.user_path() + "/" + pdf
    
    def note_path(self, pdf:str, note:str):
        return self.notes_path(pdf) + "/" + note + ".json"

    def authenticate(self, strUser: str) -> bool:
        self.selected = strUser
        try:
            os.mkdir(self.user_path())
        except:
            pass
        return True
    
    def get_pdfs(self) -> list[str]:
        #this is fine if PDFs aren't updated at runtime
        return list(self.pdfs.keys())
    
    def get_pdf_path(self, strFileName: str) -> str:
        if strFileName in self.pdfs:
            return self.pdfs[strFileName]
        else:
            return super().get_pdf_path(strFileName)
    
    def get_notes(self, strPdf: str):
        #TODO more robust error checking
        try:
            print(self.notes_path(strPdf))
            path = self.notes_path(strPdf)
            try:
                os.mkdir(path)
                print("created path for notes")
                return super().get_notes(strPdf)
            except:
                files = [file for file in os.listdir(path) if os.path.isfile(path+'/'+file)]
                print("files: ")
                [print(file) for file in files]
                # split file name
                return [os.path.splitext(file)[0] for file in files]
        except IOError as e: 
            print("error finding notes")
            print(e)
            return super().get_notes(strPdf)
    
    def get_note_file(self, strPdf: str, strFile: str) -> dict[str, Any]:
        path = self.note_path(strPdf, strFile)
        try:
            f = open(path, "r")
            data:str = f.read()
            return json.loads(data)
        except:
            return super().get_note_file(strPdf, strFile)
    
    def send_note(self, strPdf: str, strFile: str, json_note: dict[str, Any]) -> bool:
        #ensure path exists before saving note
        try:
            os.mkdir(self.notes_path(strPdf))
        except:
            pass

        path = self.note_path(strPdf, strFile)
        try:
            f = open(path, "w")
            f.write(json.dumps(json_note))
            return True
        except: 
            return False
