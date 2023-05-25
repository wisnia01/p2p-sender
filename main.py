import tkinter as tk
from tkinter import Text, Label, Button
from tkinter import filedialog
import ecb_methods as ecb
import cbc_methods as cbc
import helpers
import os
import PyPDF2
import socket


def upload_file():
    #here replace it with askopenfile but i dont bother for now
    filename = filedialog.askopenfilename()
    filename = filename.split('/')[len(filename.split('/'))-1]
    file_label['text'] = filename

#AES Implementation
key = b'Sixteen byte key'
iv = b'This is an IV456'

plaintext = b'This is a secret message.'


def main():
    print("start")
    print(ecb.decrypt_ecb(ecb.encrypt_ecb(plaintext, key),key))

    print("cbc now")
    iv, cipher = cbc.encrypt_cbc(plaintext, key)
    print(cbc.decrypt_cbc(cipher, key, iv))
    output_directory = "outputs/"

    print("test loading pdf file")
    pdf = PyPDF2.PdfReader(open("test_files/ENG_SCS_23_project.pdf", "rb"))
    print(pdf)
    for page_number in range(len(pdf.pages)):
        print(page_number)
        pdf_writer = PyPDF2.PdfWriter()
        page = pdf.pages[page_number]
        pdf_writer.add_page(page)
        part_pdf_filename = f"testfile_{page_number}.pdf"
        output_filepath= os.path.join(output_directory, part_pdf_filename)
        with open(output_filepath, 'wb') as output_file:
            pdf_writer.write(output_file)
            output_file.close()


    
    print("TCP_test")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))
    client_socket, client_address = server_socket.accept()
    print('Client connected:', client_address)

    # Receive data from the client
    data = client_socket.recv(1024)
    print('Received data:', data.decode())

    # Send a response back to the client
    response = 'Message received'
    client_socket.send(response.encode())

    # Close the client socket
    client_socket.close()


    print("GUI")
    root = tk.Tk()

    # set properties of the window
    root.title("BSK Project")

    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # textbox for inputting text
    textbox = Text(root, height=5, width=70, pady = 10)
    label = Label(root, text = "Type a message")

    # uploading files
    upload_file_button = Button(root, text = "Upload file", command = lambda:upload_file())
    file_label = Label(text='Choose a file')

    send_button = Button(root, text = "Send", )
    exit_button = Button(root, text = "Exit", command = root.destroy)

    label.pack()
    textbox.pack()
    upload_file_button.pack()
    file_label.pack()
    send_button.pack()
    exit_button.pack()

    root.mainloop()

    print("stop")


if __name__ == "__main__":
    main()