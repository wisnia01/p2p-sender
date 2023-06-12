import socket
import helpers
import json
import rsa_methods as rsa
import cbc_methods as cbc

class User:
    
    def __init__(self, host, sendport, recivport):
        self.host = host
        self.sendport = sendport
        self.recivport = recivport
        self.public_key, self.private_key = rsa.generate_rsa_keys()
        self.friends_pubkey = None
        self.last_message = None
        self.session_key = None
        
    def send_message(self, message, type="message"):
        data = {
            'Content-Type': type,
            'Message': message
        }
        json_string = json.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.sendport))
        s.sendall(json_string.encode())
        s.close()

    def receive_message(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, self.recivport))
            s.listen(1)
            conn, addr = s.accept()
            json_string = conn.recv(1024).decode()
            data = json.loads(json_string)
            if data["Content-Type"]=="pubkey":
                self.friends_pubkey=data["Message"]

            elif data["Content-Type"]=="sessionkey":
                self.session_key=rsa.decrypt_message_with_privatekey(data["Message"], self.private_key)
            else:
                print("Received message:", data["Message"])
                self.last_message = data["Message"]
            conn.close()
            s.close()
        
    def send_pubkey(self):
        self.send_message(self.public_key.decode('utf-8'), type="pubkey")
        print(self.public_key.decode('utf-8'))
    
    def send_sessionkey(self):
        encrypted_sessionkey = rsa.encrypt_message_with_publickey(self.session_key, self.friends_pubkey)
        self.send_message(encrypted_sessionkey, type="sessionkey")
    
    def create_connection_with_friend(self):
        self.session_key = helpers.generate_random_key(16)
        self.send_pubkey()
        self.send_sessionkey()