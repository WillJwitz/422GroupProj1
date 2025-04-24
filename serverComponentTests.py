from abstractServerComponent import abstract_server_component
from memoryServerComponent import memory_server_component
from localServerComponent import local_server_component

from typing import Any

def test_save_load(server: abstract_server_component):
    data:dict[str, Any] = {}
    data["Title"] = "Hello World"
    data["Body"] = "This is a note file!"

    server.authenticate("user_1")

    pdf:str = server.get_pdfs()[0]

    server.send_note(pdf, "notes", data)

    new_data = server.get_note_file(pdf, "notes")

    assert(new_data["Title"] == data["Title"])
    assert(new_data["Body"] == data["Body"])
    print(new_data["Title"])

def test_component(server_source, name:str):
    print("begin testing: "+name)
    print("begin save/load test: "+name)
    test_save_load(server_source())
    print("end save/load test: "+name)
    print("end testing: "+name)

def main():
    test_component(lambda: memory_server_component(), "memory server component")
    

if __name__ == "__main__":
    main()