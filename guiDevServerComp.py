from abstractServerComponent import AbstractServerComponent

class guiServerComponent(AbstractServerComponent):

    def __init__(self):
        super().__init__()

    # All super().--- calls are temporary
    def boolAuthenticate(self, strUser):
        return super().boolAuthenticate(strUser)
    
    def listGetPdf(self):
        return super().listGetPdf()
    
    def strGetPdfPath(self, strFileName):

        '''
        Need to fill this in to return path to pdf.
        For right now can probably just hard code a path
        to a test pdf and return that. Eventually this stuff
        will be getting handeled by the backend.
        '''

        return super().strGetPdfPath(strFileName)
    
    def listGetNotes(self, strPdf):
        return super().listGetNotes(strPdf)
    
    def jsonGetNoteFile(self, strPdf, strFile):
        return super().jsonGetNoteFile(strPdf, strFile)
    
    def boolSendNote(self, jsonNote):

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

        return super().boolSendNote(jsonNote)