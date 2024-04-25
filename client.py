from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huffmanCode.huffman import HuffmanCoding
import json
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
import os
fastAPI = FastAPI()
h = HuffmanCoding()


class Format(BaseModel):
    content: str
    filename: str

def connection ():
    import socket
    app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app.connect(("127.0.0.1", 1700))
    return app

# allow the connection between the client and the server
fastAPI.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##########################################################
##########################################################
##########################################################


# upload a file to the server

@fastAPI.post("/upload")
async def upload(file: UploadFile = File(...)):    
    try:
        app = connection()
        # Notify the server that a file will be sent
        app.send('1'.encode()) 
     
        # Send the filename to the server
        print("filename: ", file.filename)
        app.send(file.filename.encode('utf-8'))
        print("the original file size is: " , file.size , "bytes")

        
        # Send the file content to the server
        ready_signal = app.recv(1).decode()
        if ready_signal == "2":
         file_content = await file.read()
         app.sendall(file_content)
        
        # Notify the server that file transfer is complete
        #app.send('4'.encode())
         
        
         print("File sent to server successfully")
        else:
         print("Server is not ready to receive file content")
        
    except Exception as e:
        print(e)
        return {"error": f"An error occurred: {str(e)}"}


        

##########################################################
##########################################################
##########################################################

# get all the files in the directory 

def getFile(app):
    size = ""
    
    while True:
        result = app.recv(1).decode()
        
        if result == "|":
            break;
        
        size += result
    
    
    if size == "0":
        return "fini"
    else :
        size = int(size)
        filename = app.recv(size).decode()

    return filename


@fastAPI.get("/getFiles")
async def getFiles():
    listFiles = []

    app = connection()
    app.send('2'.encode())
    
    while True:
        filename = getFile(app)
        
        if filename == "fini":
            break;
        
        listFiles.append(filename)
    app.send('4'.encode())
    # print(listFiles)

    return listFiles
    
##########################################################
##########################################################
##########################################################
class FilenameRequest(BaseModel):
    filename: str
    
@fastAPI.post("/downFile")
async def downFile(filename_request: FilenameRequest):
    filename = filename_request.filename
    
    
    app = connection()
    
    app.send('3'.encode())
    app.send(filename.encode('utf-8'))
    print("filename: ", filename)
    print("Send the filename to the server")

    # Receive the size of the file content
    file_size = int(app.recv(1024).decode('utf-8'))
        
    # Send acknowledgment back to the server
        
    # Receive the file content
    received_file_content = b""
    while len(received_file_content) < file_size:
            chunk = app.recv(1024)
            # print("chunk: ", chunk)
            received_file_content += chunk
            
    

        
    
    app.send('ok'.encode())

    
  


    reverse_mapping_json =   app.recv(1024).decode('utf-8')
    print('All information of the file from the server has been received successfully.')



# Load the JSON string
    reverse_mapping = None
    try:
     reverse_mapping = json.loads(reverse_mapping_json)

    except json.JSONDecodeError as e:
     print("Error decoding JSON:", e)

  

    h = HuffmanCoding()
    if reverse_mapping != None:
        decompressed_text = h.decompress( received_file_content ,reverse_mapping )
        if decompressed_text != None:
             print("Decompressed file text successfully") 
           
    # Convert decompressed text to bytes
    
        decompressed_bytes = decompressed_text.encode("utf-8")
        
        # Create a BytesIO object to stream the bytes
        file_stream = BytesIO(decompressed_bytes)
        
        print("File stream created successfully: Sent to the browser in progress...")

        
        # Return the file as a streaming response
        # StreamingResponse in FastAPI doesn't save a file ; instead, it sends the file content directly to the client as a stream.
        app.send('4'.encode())
        

        return StreamingResponse(file_stream, media_type="text/plain",
                                 headers={"Content-Disposition":
                                     f"attachment; filename={filename.split('.')[0]}.txt"})
        
    else:
        app.send('4'.encode())
        print("Error decoding JSON")
        return "Error decoding JSON"

                

    

    
    

   




    
    
    
    
#python -m uvicorn client:fastAPI --reload
#1 pour enregistrer un fichier
#2 pour recuperer tout les fichiers
#3 pour télécharger un fichier
#4 pour fermer la connexion
    
    
