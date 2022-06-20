import socket
import threading
import re
import random
from tkinter import *

# TODO esm haro ye taghir asasi bede
# TODO be class hat vorudi bede
# ------------------------------Functions-------------------------------

# <-------Check True Validation------->
def check_valid(win,SERVER, IP, PORT, NAME):
    ip_pattern = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", IP)
    name_pattern = re.match(r"[A-Za-z1-9]", NAME)

    if ip_pattern and PORT.isdigit() and name_pattern:
        return SERVER.connect_to_server(win, IP, int(PORT), NAME)
    else:
        # TODO fix error message
        print('error')
        return False,"That's incorrect"

# <-------Unique Color------->
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color

# ------------------------------Classes-------------------------------

# <-------Server Class------->
# TODO change this name ??
class Server:
    def __init__(self, soc:socket.socket, window):
        self.soc = soc
        self.window=window
        self.RoomID = ''
        self.UserName = ''
        self.Color = random_color()

    def connect_to_server(self,win, IP: str, PORT: int, NAME: str):
        try:
            self.soc.connect((IP, PORT))
            # Send username and get response from server
            data = f'connect {NAME}'.encode('utf-8')
            print(data)
            self.soc.sendall(data)
            response = str(self.soc.recv(1024), 'utf-8').split(' ')
            self.UserName = response[0]
            self.window.insert_listbox(int(response[1]))
            self.window.rooms_frame()
            win.destroy()
            threading.Thread(target=self.client_recv).start()
        except:
            print('Something is wrong!')
            win.destroy()

    def client_send_message(self, msg):
        data = f'message {msg} {self.UserName} {self.Color} {self.RoomID}'
        try:
            self.soc.sendall(data.encode('utf-8'))
        except socket.error:
            # TODO error message haro dorost neshun bede
            print('Server is down!')
    
    def client_create_room(self):
        data = f'create {self.UserName}'
        try:
            self.soc.sendall(data.encode('utf-8'))
            self.window.room_frame.destroy()
            self.window.chats_frame()
        except socket.error:
            # TODO error message haro dorost neshun bede
            print('Server is down!')

    def client_recv(self):
        while True:
            data = str(self.soc.recv(1024), 'utf-8').split(' ')
            server_method = data[0]
            if server_method == 'create':
                self.RoomID = data[1]
            elif server_method == 'message':
                server_message = data[1]
                server_username = data[2]
                server_color = data[3]
                server_roomID = data[4]
                if self.RoomID != server_roomID :
                    continue

                # Custom tag color for print with diffrent color
                self.window.MESSAGEBOX.tag_config(f'{server_username}', foreground=server_color)

                # Insert message in messagebox 
                self.window.MESSAGEBOX.configure(state='normal')
                if server_username == self.UserName:
                    self.window.MESSAGEBOX.insert(END, f'Me: {server_message}\n')
                else:
                    self.window.MESSAGEBOX.insert(INSERT, f'{server_username}: {server_message}\n', f'{server_username}')
                self.window.MESSAGEBOX.configure(state='disabled')
            
# <-------Window Class------->
class Window:
    def __init__(self,server:Server,master:Tk, title:str,geometery:str):
        self.server=server
        # Main window attr
        self.master = master
        master.title(title)
        master.geometry(geometery)
        # Variables
        self.IP=StringVar(master)
        self.PORT = StringVar(master)
        self.USERNAME = StringVar(master)
        self.MESSAGE = StringVar(master)
        # Frames
        self.room_frame = Frame(master)
        self.chat_frame = Frame(master)
        # Login Button
        self.login_btn= Button(master,text='Login',command=self.login_window)
        self.login_btn.grid(column=2,row=2)
        # Listbox room & dounble click event
        self.ROOMS_LIST = Listbox(self.room_frame)
        self.ROOMS_LIST.bind('<Double-1>',self.double_ckick_event)
        self.MESSAGEBOX = Text(self.chat_frame) 

    def login_window(self):
        # login window attr
        win = Toplevel(self.master)
        win.title('Login')
        win.geometry('200x200')
        # login window items
        Label(win, text='Enter your IP').pack()
        Entry(win, textvariable=self.IP).pack()
        Label(win, text='Enter your Port').pack()
        Entry(win, textvariable=self.PORT).pack()
        Label(win, text='Enter your Username').pack()
        Entry(win, textvariable=self.USERNAME).pack()
        Button(win, text='save', command=lambda: check_valid(win,self.server ,self.IP.get(), self.PORT.get(), self.USERNAME.get())).pack()

    def rooms_frame (self):
        # TODO show username
        self.login_btn.destroy()
        self.room_frame.pack()
        # Rooms' frame items
        Label(self.room_frame, text='Avabaile Rooms:').pack()
        self.ROOMS_LIST.pack()
        Button(self.room_frame,text='Create Room',command=lambda:self.server.client_create_room()).pack()
    
    def chats_frame (self):
        # TODO show username and room's number
        self.chat_frame.pack()
        # Chats' frame items
        Entry(self.chat_frame,textvariable=self.MESSAGE, width=50).pack()
        Button(self.chat_frame,text='Send', command=lambda: self.server.client_send_message(self.MESSAGE.get())).pack()
        self.MESSAGEBOX.pack()
    
    def insert_listbox(self,num:int):
        for i in range(num):
            self.ROOMS_LIST.insert(i+1,f"Room's {i+1}")
    
    def double_ckick_event(self,event):
        selected_room = self.ROOMS_LIST.curselection()
        self.server.RoomID = str(selected_room[0]+1)       
        self.room_frame.destroy()
        self.chats_frame()


# ------------------------------Main-------------------------------

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tk = Tk()
server = Server(soc)
win = Window(server,tk,"323's Room","400x400")
tk.mainloop()
