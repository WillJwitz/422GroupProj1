from abstractServerComponent import AbstractServerComponent

class DummyServerComponent(AbstractServerComponent):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.pdfs = {"test": "/TestDummies/test.pdf"};
        self.selected = ""

    # All super().--- calls are temporary
    def boolAuthenticate(self, strUser: str) -> bool:
        return super().boolAuthenticate(strUser)
        self.selected = strUser
    
    def listGetPdf(self) -> list[str]:
        return list(self.pdfs.keys())
        
    
    def strGetPdfPath(self, strFileName: str) -> str:
        if strFileName in self.pdfs:
            return self.pdfs[strFileName]
        else:
            return super().strGetPdfPath(strFileName)
    
    def listGetNotes(self, strPdf: str):
        if not self.selected in self.data:
            return super().listGetNotes(strPdf)
        noteGroups = self.data[self.selected]
        if not strPdf in noteGroups:
            return super().listGetNotes(strPdf)
        return list(noteGroups[strPdf])
    
    def jsonGetNoteFile(self, strPdf: str, strFile: str):
        if not self.selected in self.data:
            return super().listGetNotes(strPdf)
        noteGroups = self.data[self.selected]
        if not strPdf in noteGroups:
            return super().listGetNotes(strPdf)
        notes = noteGroups[strPdf]
        if not strFile in notes:
            return super().listGetNotes(strPdf)
        return notes[strFile]
    
    def boolSendNote(self, jsonNote) -> bool:
        #I think we have a specification bug
        #the params don't include where the note goes
        return False
