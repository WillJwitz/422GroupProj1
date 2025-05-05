"""
Team 2: Team Sprinkles
Abstract Document Storage Class
Document Storage Module
Sawyer Christenssen, Drew Christie, Hayden Houlihan, William Jurewitz, Kaleo Montero
Last edited --- 4/23/2025
"""

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
        return []

  
    @abstractmethod
    def get_pdf_path(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_notes(self, pdfName: str) -> list[str]:
        return []

    @abstractmethod
    def get_note_file(self, pdfName: str, noteName: str) -> dict[str, Any]:
        return {}

    @abstractmethod
    def send_note(self, pdfName: str, noteName: str, jsonNote: dict[str, Any]) -> bool:
        pass
