from abc import ABC, abstractmethod  # Imports for abstract class
from typing import Any

class abstract_server_component(ABC):
    # Abstract class for Server component
    # Facilitates communication between the GUI
    # and the server components
    
    @abstractmethod
    def __init__(self):
        super().__init__()
        self._store: dict[str, dict[str, dict[str, Any]]] = {} # levels: user, pdf name, note file name, note contents
        self._pdfs: dict[str, str] = {"test": "/TestDummies/test.pdf"}


    @abstractmethod
    def authenticate(self, username: str) -> bool:
        #func authenticate
        #takes a string, returns boolean (isLoggedIn)
        self._user = username
        self._store.setdefault(username, {})
        return True

# PDFs --------------------------------
    @abstractmethod
    def get_pdfs(self) -> list[str]:
        #func get/list pdfs from server
        #takes no arguments, returns a list of names
        return list(self._pdfs.keys())

  
    @abstractmethod
    def get_pdf_path(self, filename: str) -> str:
        #func get pdf file
        #input is file name (string), output is (string)
        try:
            return self._pdfs[filename]
        except KeyError as exc:
            raise FileNotFoundError(f"No PDF named '{filename}'.") from exc

# Notes --------------------------------
    @abstractmethod
    def get_notes(self, pdfName: str) -> list[str]:
        #func get note files
        #takes a string (pdf)
        user = self._user #NEED TO BE AUTHENTICATED FIRST
        return list(self._store[user].get(pdfName, {}).keys())

    @abstractmethod
    def get_note_file(self, pdfName: str, noteName: str) -> dict[str, Any]:
        #func get note file
        #takes 2 strings, pdf and file name, return json object
        user = self._user #NEED TO BE AUTHENTICATED FIRST
        try:
            return self._store[user][pdfName][noteName]
        except KeyError as exc:
            raise FileNotFoundError(f"No note '{noteName}' for PDF '{pdfName}'.") from exc

    @abstractmethod
    def send_note(self, pdfName: str, noteName: str, jsonNote) -> bool:
        #func send note
        #input note, returns boolean if it succeeded
        user = self._user #NEED TO BE AUTHENTICATED FIRST
        self._store[user].setdefault(pdfName, {})[noteName] = jsonNote
        return True
