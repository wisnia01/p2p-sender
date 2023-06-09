import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Button, Text, Label
from tkinter import filedialog 
import user as u
import helpers

class Window(tk.Tk):
    def __init__(self, user):
        super().__init__()
        
        # set properties of the window
        self.title("BSK Project")
        
        self.window_width = 1000
        self.window_height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.padding = 5
        self.background_color = "#FFDDD2"

        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.configure(bg=self.background_color)
        
        self.file_frame = tk.LabelFrame(self, text="Send a file", bg="#FFACC7", padx=self.padding, pady=self.padding, width=(self.window_width/2 - self.padding*4), height=(self.window_height/2 - self.padding*4))
        self.file_frame.grid(row=0, column=0, sticky="nsew", padx=(self.padding*3,self.padding), pady=(self.padding,self.padding))
        
        self.message_frame = tk.LabelFrame(self, text="Send a message", bg="#FFB9B9", padx=self.padding, pady=self.padding, width=(self.window_width/2 - self.padding*4), height=(self.window_height/2 - self.padding*4))
        self.message_frame.grid(row=1, column=0, sticky="nsew", padx=(self.padding*3,self.padding), pady=(self.padding,self.padding))
        
        self.receive_frame = tk.LabelFrame(self, text="Received messages", bg="#FF8DC7", padx=self.padding, pady=self.padding, width=(self.window_width/2 - self.padding*4), height=(self.window_height - self.padding*4))
        self.receive_frame.grid(row=0, column=1, rowspan=2,sticky="nsew", padx=(self.padding*2,self.padding), pady=(self.padding,self.padding)) 

        self.create_widgets()
        
        self.receive_frame.grid_propagate(0)
        
        self.user = user
        self.actual_received_messages = 0


    def create_widgets(self):
        # ! File frame widgets !
        self.filename = "No file selected."
        tk.Button(self.file_frame, background="white", padx=self.padding*8, text = "Upload file", command=self.upload_file).grid(row=0, column=0, pady=self.padding*4)
        self.file_label = tk.Label(self.file_frame, text=self.filename, justify=tk.LEFT, width=39, background="#FFACC7", padx=self.padding)
        self.file_label.grid(row=0, column=1, padx=self.padding*2)
        
        #menu for choosing the encryption algorithm
        self.file_algorithm = tk.IntVar()
        self.file_algorithm.set(1)
        tk.Label(self.file_frame, text="Choose algorithm", justify=tk.LEFT, padx=self.padding, background="#FFACC7").grid(row=1, column=0, sticky='nw')
        tk.Radiobutton(self.file_frame, text="ECB", indicatoron=0, padx=self.padding*8, variable=self.file_algorithm, value=1, background="#FFACC7").grid(row=2, column=0, sticky='nw', pady=self.padding)
        tk.Radiobutton(self.file_frame, text="CBC", indicatoron=0, padx=self.padding*8, variable=self.file_algorithm, value=2, background="#FFACC7").grid(row=3, column=0, sticky='nw', pady=self.padding)

        tk.Button(self.file_frame, background="white", padx=self.padding*6, text = "Submit", command=self.send_encrypted_file).grid(row=4, column=0, columnspan=2, sticky='se', pady=self.padding*5)
        
        self.progress = tk.IntVar()
        self.progress.set(0)
        self.progressbar = ttk.Progressbar(self.file_frame, length=((self.window_width/2) - 50), maximum=101, variable=self.progress, orient='horizontal', mode='determinate')
        self.progressbar.grid(row=5, column=0, columnspan=2)
        
        # ! Message frame widgets !
        # textbox for inputting text
        self.message_textbox = tk.Text(self.message_frame, height=16, width=55)
        self.message_textbox.grid(row=0, column=0, sticky="nsew", padx=self.padding, pady = self.padding*2)
        
        #menu for choosing the encryption algorithm
        self.message_algorithm = tk.IntVar()
        self.message_algorithm.set(1)
        tk.Label(self.message_frame, text="Choose algorithm", justify=tk.LEFT, padx=self.padding, background="#FFB9B9").grid(row=1, column=0, sticky='w', pady=self.padding)
        tk.Radiobutton(self.message_frame, text="ECB", indicatoron=0, padx=self.padding*8, variable=self.message_algorithm, value=1, background="#FFB9B9").grid(row=2, column=0, sticky='w', pady=self.padding)
        tk.Radiobutton(self.message_frame, text="CBC", indicatoron=0, padx=self.padding*8, variable=self.message_algorithm, value=2, background="#FFB9B9").grid(row=3, column=0, sticky='w', pady=self.padding)
        
        tk.Button(self.message_frame, background="white", padx=self.padding*6, text = "Submit", command=self.send_encrypted_message).grid(row=4, column=0, sticky='e', pady=self.padding*2)
        
        # ! Receive frame widgets !
        # show last 5 messages in the box
        self.last_messages = [tk.Label(self.receive_frame, text=" ", justify=tk.LEFT, padx=self.padding, background="#FF8DC7") for i in range(20)]
        
        for idx, message in enumerate(self.last_messages):
            message.grid(row=idx, column=0, columnspan=2, sticky='w', pady=self.padding)
        
        tk.Button(self.receive_frame, background='white', padx=self.padding*8, text = "Send public key", command=self.send_pubkey).grid(row=21, column=0, pady=self.padding*4)
        tk.Button(self.receive_frame, background='white', padx=self.padding*12, text = "Connect", command=self.create_connection_with_friend).grid(row=22, column=0, pady=self.padding)
        
        self.connect_label = tk.Label(self.receive_frame, text="Not connected.", padx=self.padding*4, background="#FF8DC7")
        self.connect_label.grid(row=22, column=1, pady=self.padding)
        
    def upload_file(self):
        self.filename = filedialog.askopenfilename()
        if len(self.filename) < 52:
            self.file_label['text'] = self.filename
        else:
            # if file name is too long to display
            overflow = len(self.filename) - 52
            shortened_label = self.filename[overflow:]
            shortened_label = ".." + shortened_label[2:]
            self.file_label['text'] = shortened_label
    
    def send_encrypted_file(self):
        if(self.filename != "No file selected."):
            file = helpers.read_file(self.filename)
            file_extension = os.path.splitext(self.filename)[1]
            name = os.path.basename(self.filename).split(".")[0]
            
            if self.file_algorithm.get() == 1:
                self.user.send_file(file, file_extension, name, self.progress, method="ecb")
            elif self.file_algorithm.get() == 2:
                self.user.send_file(file, file_extension, name, self.progress, method="cbc")
            
        
    def send_encrypted_message(self):
        message = self.message_textbox.get(1.0, "end-1c")
        if(message != ""):
            if self.message_algorithm.get() == 1:
                self.user.send_encrypted_message(message, method="ecb")
            elif self.message_algorithm.get() == 2:
                self.user.send_encrypted_message(message, method="cbc")
    
    def update_messages(self):
        if self.actual_received_messages != self.user.received_messages:
            for idx in range(len(self.last_messages)-1, 0, -1):
                self.last_messages[idx]['text'] = self.last_messages[idx-1]['text']
                
            self.last_messages[0]['text'] = self.user.last_message
            self.actual_received_messages = self.actual_received_messages + 1
        self.after(1000, self.update_messages)

    def send_pubkey(self):
        if(self.connect_label['text'] != "Connected."):
            self.user.send_pubkey()
    
    def create_connection_with_friend(self):
        if(self.connect_label['text'] != "Connected."):
            self.user.create_connection_with_friend()
        
    def check_if_connected(self):
        if self.user.friends_pubkey and self.user.session_key:
            self.connect_label['text'] = "Connected."
        self.after(1000, self.check_if_connected)