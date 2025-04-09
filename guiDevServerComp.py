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
        return super().strGetPdfPath(strFileName)
    
    def listGetNotes(self, strPdf):
        return super().listGetNotes(strPdf)
    
    def jsonGetNoteFile(self, strPdf, strFile):
        return super().jsonGetNoteFile(strPdf, strFile)
    
    def boolSendNote(self, jsonNote):
        return super().boolSendNote(jsonNote)