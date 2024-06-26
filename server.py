import os
from pathlib import Path
import socket
import threading
from huffmanCode.huffman import HuffmanCoding
import json

from DataBase.createData import create_database_if_not_exists
import sqlite3  


app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app.bind(("127.0.0.1", 1700))

app.listen()


# Create a thread class to handle multiple clients
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

            
            #Action pour enregistrer un fichier : action 1 
            ##############################################
            if action == "1":

                 print("1. Enregistrer un fichier")
                 
                   # Receive the filename

                 filename_with_extension = self.client.recv(1024).decode('utf-8')
                 filename, extension = os.path.splitext(filename_with_extension)
                 print(f"Receiving file: {filename}") 
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
                         
                    # print(received_bytes)
                    # received_string = received_bytes.decode('utf-8')

                          
                    
                 output ,reverse_mapping= h.compress(received_bytes.decode('utf-8'))
                #  print(output)
                #  print(reverse_mapping)
                #  print("Compressed file path: " + file_path)
                 
                 with open(file_path, 'wb') as f:
                    f.write(output)
                
                 file_size = os.path.getsize(file_path)
                 

                 
              
                
                 reverse_mapping_json = json.dumps(reverse_mapping)

                
                # Insert data into the database
                 conn = sqlite3.connect('./DataBase/files_database.db')
                 cursor = conn.cursor()
                 cursor.execute('''INSERT INTO Fichiers (original_filename, path, reverse_mapping)
                                  VALUES (?, ?, ?)''', (filename,  str(file_path), reverse_mapping_json))
                 conn.commit()
                 conn.close()
                
                    
                

                 print(f"File saved successfully.  File size after compress: {file_size} bytes")
                 
            # envoie la liste des fichiers action 2
            #######################################
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
                # print("Liste des fichiers envoyée au client avec succès")
                        
            
                
            #Action pour télécharger un fichier : action 3
            ##############################################
            elif action == "3":
             print("3. Télécharger un fichier")
    
             # Receive the filename from the client
             filename_with_extension = self.client.recv(1024).decode('utf-8')
             filename, extension = os.path.splitext(filename_with_extension)

             print(f" file name: {filename}")
    
              # Get the file path and reverse_mapping from the database
             conn = sqlite3.connect('./DataBase/files_database.db')
             cursor = conn.cursor()
             cursor.execute("SELECT path, reverse_mapping FROM Fichiers WHERE original_filename = ?", (filename,))
             result = cursor.fetchone()
             print("get the file info from the database")
            #  print(result)
             file_path = result[0]
             reverse_mapping = result[1] 
             conn.close()
             

             
         
             

    
             # Send the file content to the client
             with open(file_path, 'rb') as file:
                 print("Sending file content to the client .. ")

                 file_content = file.read()
                #  print(file_content)
                 file_size = len(file_content)
                #  print("the original file size is: " , file_size , "bytes")
                
                 self.client.sendall(str(file_size).encode())
                 
                 self.client.sendall(file_content)
                 
      

             
             # Send the reverse_mapping to the client
             
 
             if self.client.recv(2).decode('utf-8') == "ok":
   
                self.client.sendall(reverse_mapping.encode())
                print(" All File info sent to client in successfully")


             
       
    
             
             
            

                
                
            #Action pour fermer la connexion : action 4
            ###########################################
            elif action == "4":
                self.client.close()
                break;


while True:
    client, _ = app.accept()
    thread = Thread(client)
    thread.start()