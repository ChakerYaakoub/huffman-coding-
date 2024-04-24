# File Compression and Decompression Project

This project implements a client-server architecture using TCP/IP communication and Huffman coding for file compression and decompression.

## Installation

Open your terminal or command prompt.

Navigate to the root directory of your project.

Run the following command to install all the required packages:

```bash
pip install -r requirements.txt
```


## Running the Server : terminal 1

To start the server, run the following command:
```bash
python server.py
```



## Running the Client : terminal 2

To start the client interface, run the following command:

```bash
python -m uvicorn client:fastAPI --reload
```



This will launch a live server for the client interface.

## Accessing the Client Interface

To access the client interface, open the `index.html` file in your web browser. The interface allows you to upload files for compression and decompression using the server's functionalities.

## Project Structure

- `server.py`: Python script for the server implementation.
- `client.py`: Python script for the client implementation.
- `./huffmanCode/huffman.py`: Python script containing the Huffman coding algorithm implementation.
- `index.html`: HTML file for the client interface.
- `DataBase`: Folder containing scripts to create database.
- `files`: Folder containing all the compressed files '.bin'.




## Dependencies

- Python 3.x
- FastAPI
- Uvicorn



