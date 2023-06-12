import tkinter as tk
from tkinter import *
from tkinter import filedialog

def init_gui():
    
    root = tk.Tk()

    # set properties of the window
    root.title("BSK Project")

    window_width = 1000
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    padding = 5
    background_color = "#FFDDD2"

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.configure(bg=background_color)
    
    file_frame = tk.LabelFrame(root, text="Send a file", bg="#FFACC7", padx=padding, pady=padding, width=(window_width/2 - padding*4), height=(window_height/2 - padding*4))
    file_frame.grid(row=0, column=0, sticky="nsew", padx=(padding*3,padding), pady=(padding,padding))
    #file_frame.grid_rowconfigure(1, weight=1)
    
    message_frame = tk.LabelFrame(root, text="Send a message", bg="#FFB9B9", padx=padding, pady=padding, width=(window_width/2 - padding*4), height=(window_height/2 - padding*4))
    message_frame.grid(row=1, column=0, sticky="nsew", padx=(padding*3,padding), pady=(padding,padding))
    #message_frame.grid_rowconfigure(0, weight=1)
    
    receive_frame = tk.LabelFrame(root, text="Received messages and files", bg="#FF8DC7", padx=padding, pady=padding, width=(window_width/2 - padding*4), height=(window_height - padding*4))
    receive_frame.grid(row=0, column=1, rowspan=2,sticky="nsew", padx=(padding*2,padding), pady=(padding,padding)) 
    
    # ! File frame widgets !
    filename = "No file selected."
    tk.Button(file_frame, background="white", padx=padding*8, text = "Upload file", ).grid(row=0, column=0, pady=padding*4)
    tk.Label(file_frame, text=filename, justify=tk.LEFT, width=39, background="#FFACC7", padx=padding).grid(row=0, column=1, padx=padding*2)
    #menu for choosing the encryption algorithm
    file_algorithm = tk.IntVar()
    tk.Label(file_frame, text="Choose algorithm", justify=tk.LEFT, padx=padding, background="#FFACC7").grid(row=1, column=0, sticky='nw')
    tk.Radiobutton(file_frame, text="ECB", indicatoron=0, padx=padding*8, variable=file_algorithm, value=1, background="#FFACC7").grid(row=2, column=0, sticky='nw', pady=padding)
    tk.Radiobutton(file_frame, text="CBC", indicatoron=0, padx=padding*8, variable=file_algorithm, value=2, background="#FFACC7").grid(row=3, column=0, sticky='nw', pady=padding)

    tk.Button(file_frame, background="white", padx=padding*6, text = "Submit", ).grid(row=4, column=0, columnspan=2, sticky='se', pady=padding*10)
    
    # ! Message frame widgets !
    # textbox for inputting text
    tk.Text(message_frame, height=16, width=55).grid(row=0, column=0, sticky="nsew", padx=padding, pady = padding*2)
    
    #menu for choosing the encryption algorithm
    message_algorithm = tk.IntVar()
    tk.Label(message_frame, text="Choose algorithm", justify=tk.LEFT, padx=padding, background="#FFB9B9").grid(row=1, column=0, sticky='w', pady=padding)
    tk.Radiobutton(message_frame, text="ECB", indicatoron=0, padx=padding*8, variable=message_algorithm, value=1, background="#FFB9B9").grid(row=2, column=0, sticky='w', pady=padding)
    tk.Radiobutton(message_frame, text="CBC", indicatoron=0, padx=padding*8, variable=message_algorithm, value=2, background="#FFB9B9").grid(row=3, column=0, sticky='w', pady=padding)
    
    tk.Button(message_frame, background="white", padx=padding*6, text = "Submit", ).grid(row=4, column=0, sticky='e', pady=padding*2)
    
    # ! Receive frame widgets !
    tk.Label(receive_frame, text="Unga bunga", justify=tk.LEFT, padx=padding, background="#FF8DC7").grid(row=0, column=0, sticky='w', pady=padding)
    
    receive_frame.grid_propagate(0)

    root.mainloop()
