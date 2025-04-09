from abc import ABC, abstractmethod  # Imports for abstract class

class AbstractServerComponent(ABC):
    # Abstract class for Server component
    # Facilitates communication between the GUI
    # and the server components
    
    @abstractmethod
    def boolAuthenticate(self, strUser):
        #func authenticate
        #takes a string, returns boolean (isLoggedIn)
        pass

    @abstractmethod
    def listGetPdf(self):
        #func get/list pdfs from server
        #takes no arguments, returns a list of names
        pass

  
    @abstractmethod
    def strGetPdfPath(self, strFileName):
        #func get pdf file
        #input is file name (string), output is (string)
        pass

    @abstractmethod
    def listGetNotes(self, strPdf):
        #func get note files
        #takes a string (pdf)
        pass

    @abstractmethod
    def jsonGetNoteFile(self, strPdf, strFile):
        #func get note file
        #takes 2 strings, pdf and file name, return json object
        pass

    @abstractmethod
    def boolSendNote(self, jsonNote):
        #func send note
        #input note, returns boolean if it succeeded
        pass
