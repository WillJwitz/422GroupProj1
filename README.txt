# 422GroupProj1
# Team Sprinkles: Sawyer Christenssen, Drew Christie, Hayden Houlihan, William Jurewitz, Kaleo Montero
SQ3R Note Taking and PDF Association

## Overview

This application allows users to view PDFs and create, edit, and store notes associated with those PDFs. Notes and PDFs can be stored locally, in memory (for testing), or on a remote MongoDB server for multi-user access and backup.

## Features

- View and manage PDF documents
- Create, edit, and delete notes linked to PDFs
- Choose between local, in-memory, or MongoDB server storage
- Automatic fallback to local storage if the server is unavailable
- User-friendly GUI

## Architecture

- **main.py**: Entry point; selects storage backend and launches the GUI.
- **abstractDocumentStorage**: Interface for all storage backends.
- **memoryDocumentStorage**: Stores data in memory (testing).
- **localDocumentStorage**: Stores data in local files.
- **mongoDocumentStorage**: Stores data on a MongoDB server.
- **interfaceComponent**: GUI logic.
- **defaultConfigs**: Provides default configuration options.

## Storage Backends

- **In-Memory**: Fast, for testing; data lost on exit.
- **Local**: Stores PDFs and notes on disk.
- **MongoDB**: Stores PDFs and notes on a remote server using MongoDB and GridFS.

## Configuration

Configuration is handled via `defaultConfigs.py`. Key options include:

- `allow_server`: Enable/disable MongoDB server backend.
- `allow_local`: Enable/disable local file storage fallback.
- `server_ip`: MongoDB server IP address.
- `pdf_cache_path`: Local path for caching PDFs.

## Running the Application

1. **Install dependencies**  
   Make sure you have Python 3.8+ and the following packages:
   - `pymongo`
   - `gridfs`
   - `tkinter` (usually included with Python)

   Install with:
   ```sh
   pip install pymongo gridfs
   ```

2. **Set up MongoDB server** (optional)  
   If using the server backend, ensure your MongoDB instance is running and accessible at the configured IP and port.

3. **Run the application**
   ```sh
   python main.py
   ```

4. **Usage**
   - The app will attempt to connect to the MongoDB server if enabled.
   - If the server is unavailable and local fallback is enabled, data will be saved locally.
   - If neither is available, the app will run in memory (data lost on exit).

## Error Handling

- If the server connection fails, the app will print an error and fall back to local or in-memory storage, depending on configuration.
