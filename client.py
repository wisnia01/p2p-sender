import threading
import user as u
import cbc_methods
from Crypto.Cipher import AES

host = "localhost"
sendport = 5000
recivport = 5001

def main():
    user = u.User(host, sendport, recivport)
    receive_thread = threading.Thread(target=user.receive_message)
    receive_thread.start()
    
    print(cbc_methods.encrypt_cbc("dupa", "aaaaaaaaaaaaaaaa"))
    print(AES.block_size)
    
    
    while True:
        x = input()
        if x == "s":
            user.send_message("dupa")
        elif x == "l":
            print(user.last_message)
        elif x == "sendpubkey":
            user.send_pubkey()
        elif x == "connect":
            user.create_connection_with_friend()
        elif x == "debug":
            #print(user.public_key)
            #print(user.private_key)
            # print(user.friends_pubkey)
            print(user.session_key)
            
            


if __name__ == "__main__":
    main()