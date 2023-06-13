import socket
import helpers
import json
import rsa_methods as rsa
import cbc_methods as cbc
import ecb_methods as ecb
from Crypto.Cipher import AES

class User:
    
    def __init__(self, host, sendport, recivport):
        self.host = host
        self.sendport = sendport
        self.recivport = recivport
        self.public_key, self.private_key = rsa.generate_rsa_keys()
        self.friends_pubkey = None
        self.last_message = None
        self.session_key = None
        self.received_messages = 0
        
    def send_message(self, message, type="message", iv=None, method=None):
        data = {
            'Content-Type': type,
            'Message': message,
            'Iv': iv,
            'Method': method
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
                encrypted_message=data["Message"]
                iv = data["Iv"]
                method = data["Method"]
                if method == "cbc":
                    message = cbc.decrypt_cbc(encrypted_message, self.session_key, iv)
                elif method == "ecb":
                    message = ecb.decrypt_ecb(encrypted_message, self.session_key)
                print("Received message:", message)
                self.received_messages = self.received_messages + 1    
                self.last_message = message
            conn.close()
            s.close()
        
    def send_pubkey(self):
        self.send_message(self.public_key.decode('utf-8'), type="pubkey")
        print(self.public_key.decode('utf-8'))
    
    def send_sessionkey(self):
        encrypted_sessionkey = rsa.encrypt_message_with_publickey(self.session_key, self.friends_pubkey)
        self.send_message(encrypted_sessionkey, type="sessionkey")
    
    def create_connection_with_friend(self):
        self.session_key = helpers.generate_random_key(AES.block_size)
        self.send_pubkey()
        self.send_sessionkey()
        
    def send_encrypted_message(self, message, method="ecb"):
        iv = None
        if method == "cbc":
            iv, encrypted_message = cbc.encrypt_cbc(message, self.session_key)
        elif method == "ecb":
            encrypted_message = ecb.encrypt_ecb(message, self.session_key)
        self.send_message(encrypted_message, iv=iv, method=method)
        