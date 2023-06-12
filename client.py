import threading
import user as u
import argparse

host = "localhost"

def main(sendport, recivport):
    
    print("Podaj hosta:")
    host = input()
    user = u.User(host, sendport, recivport)
    receive_thread = threading.Thread(target=user.receive_message)
    receive_thread.start()
    
    
    while True:
        x = input()
        if x == "s":
            user.send_encrypted_message("dupa")
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
    parser = argparse.ArgumentParser()

    parser.add_argument("sendport", type=int, help="Port where the messeges are sent")
    parser.add_argument("recivport", type=int, help="Port to receive messages from another client")
    
    args = parser.parse_args()
    main(args.sendport, args.recivport)