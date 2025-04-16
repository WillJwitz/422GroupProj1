from abstractServerComponent import abstract_server_component
import os

#TODO: this should probably just be deleted now
class gui_server_component(abstract_server_component):
    #TODO: Mirror missing type hints in the abstract class.

    def __init__(self):
        super().__init__()

    # All super().--- calls are temporary
    def authenticate(self, strUser: str) -> bool:
        return super().authenticate(strUser)
    
    def get_pdfs(self) -> list[str]:
        return super().get_pdfs()
    
    def get_pdf_path(self, strFileName: str) -> str:

        '''
        Need to fill this in to return path to pdf.
        For right now can probably just hard code a path
        to a test pdf and return that. Eventually this stuff
        will be getting handeled by the backend.
        '''
        #Just returning hard-coded path for testing.
        return strFileName
        #return super().strGetPdfPath(strFileName)
    
    def get_notes(self, strPdf: str):
        return super().get_notes(strPdf)
    
    def get_note_file(self, strPdf: str, strFile: str):
        return super().get_note_file(strPdf, strFile)
    
    def send_note(self, jsonNote) -> bool:

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
        
        return super().send_note(jsonNote)
