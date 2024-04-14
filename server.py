import os
from pathlib import Path
import socket
import threading
from huffmanCode.huffman import HuffmanCoding
import json

from DataFc.createData import create_database_if_not_exists
import sqlite3  

# from huffman.huffman import HuffmanCoding

app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app.bind(("127.0.0.1", 1700))

app.listen()

create_database_if_not_exists()
class Thread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client


# receive the socket connection
    def run(self):
        while True:
            
            # action socket connection
            action = self.client.recv(1).decode()
            h = HuffmanCoding()

            
            #Action pour enregistrer un fichier
            if action == "1":

                 print("1. Enregistrer un fichier")
                 
                   # Receive the filename

                 filename_with_extension = self.client.recv(1024).decode('utf-8')
                 filename, extension = os.path.splitext(filename_with_extension)
                #  print(f"Receiving file: {filename}") 
                 # Send a signal to the client to indicate that the server is ready to receive the file content
                 self.client.send('2'.encode())
                
                # Receive and save the file content
                 received_bytes = b""
                 while True:
                    chunk = self.client.recv(1024)
                    if not chunk:
                        break
                    received_bytes += chunk
                
               
                 
                #  print(received_bytes)

                 project_root = os.getcwd()  # Get the current working directory
                #  file_path = os.path.join(project_root, 'files', filename+'.bin')
                 if not os.path.exists(os.path.join(project_root, 'files', f"{filename}.bin")):
                     file_path = os.path.join(project_root, 'files', f"{filename}.bin") 
                 else:
                    counter = 1
                    while True:
                         if not os.path.exists(os.path.join(project_root, 'files', f"{filename}_{counter}.bin")):
                              file_path = os.path.join(project_root, 'files', f"{filename}_{counter}.bin")
                              filename = f"{filename}_{counter}"
                              break
                         counter += 1
                         
                    print(received_bytes)
                    # received_string = received_bytes.decode('utf-8')

                          
                    
                 output ,reverse_mapping= h.compress(received_bytes.decode('utf-8'))
                #  print(output)
                #  print(reverse_mapping)
                #  print("Compressed file path: " + file_path)
                 
                 with open(file_path, 'wb') as f:
                    f.write(output)
                
                 file_size = os.path.getsize(file_path)
                 
              
                
                #  reverse_mapping_json = json.dumps(reverse_mapping)
                 reverse_mapping_str = str(reverse_mapping) 
                 print("\tReverse mapping: ", reverse_mapping_str)
                
                # Insert data into the database
                 conn = sqlite3.connect('files_database.db')
                 cursor = conn.cursor()
                 cursor.execute('''INSERT INTO Fichiers (original_filename, path, reverse_mapping)
                                  VALUES (?, ?, ?)''', (filename,  str(file_path), reverse_mapping_str))
                 conn.commit()
                 conn.close()
                
                    
                

                 print(f"File saved successfully.  File size: {file_size} bytes")
            
            elif action == "2":
                # Chemin du répertoire à lire
                project_root = os.getcwd() 
                directory = Path(project_root + '/files')

                for file in directory.iterdir():
                    if file.is_file():
                        filename = file.name
                        fileSize = len(filename.encode())
                        
                        self.client.send(f'{fileSize}|{filename}'.encode())
                
                self.client.send(f'0|fini'.encode())
                        
            
                
            #Action pour télécharger un fichier
            elif action == "3":
             print("3. Télécharger un fichier")
    
             # Receive the filename from the client
             filename_with_extension = self.client.recv(1024).decode('utf-8')
             filename, extension = os.path.splitext(filename_with_extension)

             print(f"Receiving file: {filename}")
    
              # Get the file path and reverse_mapping from the database
             conn = sqlite3.connect('files_database.db')
             cursor = conn.cursor()
             cursor.execute("SELECT path, reverse_mapping FROM Fichiers WHERE original_filename = ?", (filename,))
             result = cursor.fetchone()
            #  print(result)
             file_path = result[0]
             reverse_mapping = result[1] 
             conn.close()
             
            #  print("File path: ", file_path)
            #  print("Reverse mapping: ", reverse_mapping)
             
         
             

    
             # Send the file content to the client
             with open(file_path, 'rb') as file:

                 file_content = file.read()
                 print(file_content)
                 file_size = len(file_content)
                 print("the original file size is: " , file_size , "bytes")
                
                 self.client.sendall(str(file_size).encode())
                 
                 self.client.sendall(file_content)
                 
      

             
             # Send the reverse_mapping to the client
             
            #  reverse_mapping_json = json.dumps(reverse_mapping)
            #  print("\tReverse mapping: ", reverse_mapping)
             if self.client.recv(2).decode('utf-8') == "ok":
                reverse_mapping_json = json.dumps(reverse_mapping)
                print("\tReverse mapping: ", reverse_mapping)
                self.client.sendall(reverse_mapping.encode())

             
            #  test=  self.client.recv(1024).decode('utf-8')
            #  if test == "haveAFile":
            #     self.client.send('ok'.encode())
            #     self.client.sendall(reverse_mapping.encode())
             
       
    
             
             
            

                
                
            #Action pour fermer la connexion
            elif action == "4":
                self.client.close()
                break;


while True:
    client, _ = app.accept()
    thread = Thread(client)
    thread.start()