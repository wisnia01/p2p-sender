import socket
import rsa_methods as rsa

class User:
    def __init__(self, host, sendport, recivport):
        self.host = host
        self.sendport = sendport
        self.recivport = recivport
        public_key, private_key = rsa.generate_rsa_keys()
        
    def send_message(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.sendport))
        s.send(message.encode())
        s.close()

    def receive_message(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.recivport))
        s.listen(1)
        conn, addr = s.accept()
        message = conn.recv(1024).decode()
        print("Received message:", message)
        conn.close()
        s.close()
        