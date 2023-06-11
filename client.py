import threading
import user as u

host = "localhost"
sendport = 5000
recivport = 5001

def main():
    user = u.User(host, sendport, recivport)
    receive_thread = threading.Thread(target=user.receive_message)
    receive_thread.start()
    while True:
        x = input()
        if x == "s":
            user.send_message("dupa")
            

if __name__ == "__main__":
    main()