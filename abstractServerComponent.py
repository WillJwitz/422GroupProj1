from abc import ABC, abstractmethod  # Imports for abstract class

class AbstractServerComponent(ABC):
    # Abstract class for Server component
    # Facilitates communication between the GUI
    # and the server components
    
    @abstractmethod
    def __init__(self):
        super().__init__()


    @abstractmethod
    def boolAuthenticate(self, strUser: str) -> bool:
        #func authenticate
        #takes a string, returns boolean (isLoggedIn)
        pass

    @abstractmethod
    def listGetPdf(self) -> list[str]:
        #func get/list pdfs from server
        #takes no arguments, returns a list of names
        pass

  
    @abstractmethod
    def strGetPdfPath(self, strFileName: str) -> str:
        #func get pdf file
        #input is file name (string), output is (string)
        pass

    @abstractmethod
    def listGetNotes(self, strPdf: str):
        #func get note files
        #takes a string (pdf)
        #TODO: Add return type hint.
        pass

    @abstractmethod
    def jsonGetNoteFile(self, strPdf: str, strFile: str):
        #func get note file
        #takes 2 strings, pdf and file name, return json object
        #TODO: Add json type hint.
        pass

    @abstractmethod
    def boolSendNote(self, jsonNote) -> bool:
        #func send note
        #input note, returns boolean if it succeeded
        #TODO: Add json type hint.
        pass
