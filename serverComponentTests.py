"""
Team 2: Team Sprinkles
Integration tests for local and memory documetn storage
Document Storage Module
Kaleo Montero
Last edited --- 4/24/2025
"""
from abstractDocumentStorage import abstract_document_storage
from memoryDocumentStorage import memory_document_storage
from localDocumentStorage import local_document_storage

from typing import Any
import shutil

def test_save_load(server: abstract_document_storage):
    data:dict[str, Any] = {}
    data["Title"] = "Hello World"
    data["Body"] = "This is a note file!"

    server.authenticate("user_1")

    pdf:str = server.get_pdfs()[0]

    server.send_note(pdf, "notes", data)

    new_data = server.get_note_file(pdf, "notes")

    assert(new_data["Title"] == data["Title"])
    assert(new_data["Body"] == data["Body"])

def test_two_user(server: abstract_document_storage):
    data:dict[str, Any] = {}
    data["Title"] = "Hello World"
    data["Body"] = "This is a note file!"

    server.authenticate("user_1")

    pdf:str = server.get_pdfs()[0]

    server.send_note(pdf, "notes", data)


    server.authenticate("user_2")
    new_data = server.get_note_file(pdf, "notes")
    assert(new_data == {})

    server.authenticate("user_1")
    new_data = server.get_note_file(pdf, "notes")
    assert(new_data["Title"] == data["Title"])
    assert(new_data["Body"] == data["Body"])

def test_component(server_source, name:str):
    print("begin testing: "+name)
    print("begin save/load test: "+name)
    test_save_load(server_source())
    print("end save/load test: "+name)
    print("begin users test: "+name)
    test_two_user(server_source())
    print("end users test: "+name)
    print("end testing: "+name)

def main():
    test_component(lambda: memory_document_storage("TestDummies"), "memory server component")

    test_component(lambda: local_document_storage("TestDummies","TestDumps"), "local server component")
    shutil.rmtree("TestDumps")

if __name__ == "__main__":
    main()