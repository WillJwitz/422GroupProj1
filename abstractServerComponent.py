from abc import ABC, abstractmethod  # Imports for abstract class
from typing import Any

class abstract_server_component(ABC):
    # Abstract class for Server component
    # Facilitates communication between the GUI
    # and the server components
    
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def authenticate(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_pdfs(self) -> list[str]:
        pass

  
    @abstractmethod
    def get_pdf_path(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_notes(self, pdfName: str) -> list[str]:
        pass

    @abstractmethod
    def get_note_file(self, pdfName: str, noteName: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def send_note(self, pdfName: str, noteName: str, jsonNote) -> bool:
        pass
