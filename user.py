import socket
import json
import ast
import rsa_methods as rsa
import helpers

class User:
    
    def __init__(self, host, sendport, recivport):
        self.host = host
        self.sendport = sendport
        self.recivport = recivport
        self.public_key, self.private_key = rsa.generate_rsa_keys()
        self.friends_pubkey = None
        self.last_message = None
        
    def send_message(self, message, type="message"):
        data = {
            'Content-Type': type,
            'Message': message
        }
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.sendport))
        data = '\n'.join(f'{key}: {value}' for key, value in data.items())
        s.sendall(data.encode())
        s.close()

    def receive_message(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, self.recivport))
            s.listen(1)
            conn, addr = s.accept()
            data = conn.recv(1024).decode()        
            headers = helpers.create_dict_from_data(data)
            if headers["Content-Type"]=="pubkey":
                self.friends_pubkey=headers["Message"]
            print("Received message:", headers["Message"])
            self.last_message = headers["Message"]
            conn.close()
            s.close()
        
    def send_pubkey(self):
        self.send_message(self.public_key, type="pubkey")
        