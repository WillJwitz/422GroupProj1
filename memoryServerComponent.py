"""
Team 2: Team Sprinkles
Memory Document Storage Class
Document Storage Module
Sawyer Christenssen, Kaleo Montero
Last edited --- 4/24/2025
"""
from abstractServerComponent import abstract_server_component
import copy
import os

class memory_server_component(abstract_server_component):
    #A server component implementation that uses local files to store notes
    #Designed mainly for testing
    #But is the fallback for offline mode if local storage is disabled in the settings

    def __init__(self, pdfs_path: str):
        super().__init__()
        self.data = {}

        #load pdf paths into dict
        self.pdfs_path:str = pdfs_path
        files = [file for file in os.listdir(self.pdfs_path) if os.path.isfile(self.pdfs_path+'/'+file)]
        self.pdfs:dict[str, str] = {}
        for file in files:
            name = os.path.splitext(file)[0]
            self.pdfs[name] = self.pdfs_path+'/'+file
        
        self.selected = ""

    def authenticate(self, strUser: str) -> bool:
        self.selected = strUser
        if not strUser in self.data:
            self.data[strUser] = {}
        return True
    
    def get_pdfs(self) -> list[str]:
        return list(self.pdfs.keys())
        
    
    def get_pdf_path(self, strFileName: str) -> str:
        if strFileName in self.pdfs:
            return self.pdfs[strFileName]
        else:
            return super().get_pdf_path(strFileName)
    
    def get_notes(self, strPdf: str):
        if not self.selected in self.data:
            return super().get_notes(strPdf)
        noteGroups = self.data[self.selected]
        if not strPdf in noteGroups:
            return super().get_notes(strPdf)
        return list(noteGroups[strPdf])
    
    def get_note_file(self, strPdf: str, strFile: str):
        if not self.selected in self.data:
            return super().get_note_file(strPdf, strFile)
        noteGroups = self.data[self.selected]
        if not strPdf in noteGroups:
            return super().get_note_file(strPdf, strFile)
        notes = noteGroups[strPdf]
        if not strFile in notes:
            return super().get_note_file(strPdf, strFile)
        return notes[strFile]
    
    def send_note(self, strPdf: str, strFile: str, json_note) -> bool:
        if not self.selected in self.data:
            return super().get_note_file(strPdf, strFile)
        
        noteGroups = self.data[self.selected]

        if not strPdf in noteGroups:
            noteGroups[strPdf] = {}
        
        notes = noteGroups[strPdf]
        #copy so that edits to the original don't destroy saved data
        notes[strFile] = copy.deepcopy(json_note)
        return False
