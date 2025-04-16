from abstractServerComponent import abstract_server_component

class memory_server_component(abstract_server_component):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.pdfs = {"test": "/TestDummies/test.pdf"};
        self.selected = ""

    def authenticate(self, strUser: str) -> bool:
        self.selected = strUser
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
        #TODO: implement this
        return False
