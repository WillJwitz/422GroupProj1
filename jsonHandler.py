import json

def encode_note_json(note : dict) -> str:
    """Encodes input note dictionary into json string."""
    
    # indent = 4 makes file more readable if written to a file
    return json.dumps(note, indent=4)

def decode_note_json(note_json : str) -> dict:
    """Decods input json formatted string into python dict."""

    return json.loads(note_json)