import socket
import helpers
import json
import math
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
        self.num_of_reciv_files = 0
        self.num_of_already_reciv_files = 0
        self.reciv_file = ""
        
    def send_message(self, message, type="message", iv=None, method=None, file_elem="1", ext="None", file_name=""):
        data = {
            'Content-Type': type,
            'Message': message,
            'Iv': iv,
            'Method': method,
            'File_elements': file_elem,
            'File_extension': ext,
            'File_name': file_name
        }
        json_string = json.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.sendport))
        s.sendall(json_string.encode())
        s.close()

    def receive_message(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.recivport))
        while True:

            s.listen(1)
            conn, addr = s.accept()
            json_string = conn.recv(1024).decode()
            data = json.loads(json_string)
            method = data["Method"]
            encrypted_message=data["Message"]
            file_extension = data["File_extension"]
            file_name = data["File_name"]
            iv = data["Iv"]
            if data["Content-Type"]=="pubkey":
                self.friends_pubkey=data["Message"]
            elif data["Content-Type"]=="sessionkey":
                self.session_key=rsa.decrypt_message_with_privatekey(data["Message"], self.private_key)
            elif data["Content-Type"]=="file":
                self.num_of_reciv_files = data["File_elements"]
                if method == "cbc":
                    message = cbc.decrypt_cbc(encrypted_message, self.session_key, iv)
                elif method == "ecb":
                    message = ecb.decrypt_ecb(encrypted_message, self.session_key)
                self.reciv_file = self.reciv_file + message
                self.num_of_already_reciv_files = self.num_of_already_reciv_files + 1
                if self.num_of_already_reciv_files == self.num_of_reciv_files:
                    helpers.save_file("outputs/" + file_name +file_extension, self.reciv_file)
                    self.num_of_already_reciv_files = 0
                    self.num_of_reciv_files = 0
                    self.reciv_file = ""
            else:
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
        #print(self.public_key.decode('utf-8'))
    
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
        
    def send_file(self, file, ext, file_name, bar, method="ecb"):
        iv = None
        num_of_elem = math.ceil(len(file)/100)
        progress = 0
        for i in range(0, len(file), 100):
            div_element = file[i:i+100]
            
            if method == "cbc":
                iv, encrypted_message = cbc.encrypt_cbc(div_element, self.session_key)
            elif method == "ecb":
                encrypted_message = ecb.encrypt_ecb(div_element, self.session_key)
            
            self.send_message(encrypted_message, type="file", iv=iv, file_elem=num_of_elem, method=method, ext=ext, file_name=file_name)
            
            progress += 100/num_of_elem
            bar.set(progress)
            