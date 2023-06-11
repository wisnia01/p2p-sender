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
        elif x == "connect":
            user.send_pubkey()
            

if __name__ == "__main__":
    main()