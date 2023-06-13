import threading
import user as u
import argparse
import gui

host = "localhost"

def main(sendport, recivport):
    
    user = u.User(host, sendport, recivport)
    receive_thread = threading.Thread(target=user.receive_message)
    receive_thread.start()
      
    main_window = gui.Window(user)
    main_window.update_messages()
    main_window.check_if_connected()
    main_window.mainloop()
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("sendport", type=int, help="Port where the messeges are sent")
    parser.add_argument("recivport", type=int, help="Port to receive messages from another client")
    
    args = parser.parse_args()
    main(args.sendport, args.recivport)