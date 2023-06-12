import threading
import user as u

host = "localhost"
sendport = 5001
recivport = 5000

def main():
    user = u.User(host, sendport, recivport)
    receive_thread = threading.Thread(target=user.receive_message)
    receive_thread.start()
    
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
            # print(user.private_key)
            #print(user.friends_pubkey)
            print(user.session_key)
            

if __name__ == "__main__":
    main()