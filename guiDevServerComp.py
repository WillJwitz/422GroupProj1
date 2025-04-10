from abstractServerComponent import AbstractServerComponent
import os

class guiServerComponent(AbstractServerComponent):
    #TODO: Mirror missing type hints in the abstract class.

    def __init__(self):
        super().__init__()

    # All super().--- calls are temporary
    def boolAuthenticate(self, strUser: str) -> bool:
        return super().boolAuthenticate(strUser)
    
    def listGetPdf(self) -> list[str]:
        return super().listGetPdf()
    
    def strGetPdfPath(self, strFileName: str) -> str:

        '''
        Need to fill this in to return path to pdf.
        For right now can probably just hard code a path
        to a test pdf and return that. Eventually this stuff
        will be getting handeled by the backend.
        '''
        #Just returning hard-coded path for testing.
        return strFileName
        #return super().strGetPdfPath(strFileName)
    
    def listGetNotes(self, strPdf: str):
        return super().listGetNotes(strPdf)
    
    def jsonGetNoteFile(self, strPdf: str, strFile: str):
        return super().jsonGetNoteFile(strPdf, strFile)
    
    def boolSendNote(self, jsonNote) -> bool:

        '''
        Need to fill this in to save the note.
        Right now for proof of concept and getting 
        some basic functionality up and running I would
        suggest just writing it to a file for now.(?) Or 
        you could try to pack a json and save that. 
        Either way just save some stuff locally.
        Also any resources that this stuff depends on
        (test pdf) should probably be pushed to the github
        so others can test.
        '''
        #Test code for saving to test.txt
        cwd = os.getcwd()
        path = "/TestDummies/test.txt"
        with (open(cwd+path, 'w') as f):
            print(jsonNote, file=f)
        
        return super().boolSendNote(jsonNote)
