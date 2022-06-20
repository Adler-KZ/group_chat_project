import socket
import threading
import re
import random
from tkinter import *

# TODO esm haro ye taghir asasi bede

# ------------------------------Functions-------------------------------




# <-------Unique Color------->
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color
# <-------End Unique Color------->


# ------------------------------Classes-------------------------------
class server:
    global UserName
    global Color
    global RoomID

    def __init__(self, soc):
        self.soc = soc
        self.RoomID = ''
        self.Username = ''
        self.Color = random_color()


    def connect_to_server(self,win, IP: str, PORT: int, NAME: str):
        try:
            self.soc.connect((IP, PORT))
            # Send username and get response from server
            data = f'connect {NAME}'.encode('utf-8')
            print(data)
            self.soc.sendall(data)

            response = str(self.soc.recv(1024), 'utf-8').split(' ')
            UserName = response[0]
            window.insert_listbox(int(response[1]))

            window.rooms_frame()
            win.destroy()
            threading.Thread(target=self.client_recv).start()
        except:
            print('Something is wrong!')
            win.destroy()

    def client_send(self, msg):
        data = f'message {msg} {UserName} {Color} {RoomID}'
        # data = self.pack_data('message',msg,name,color)
        try:
            self.soc.sendall(data.encode('utf-8'))
        except socket.error:
            print('Server is down!')
    
    def client_create_room(self):
        #! Delete
        print(UserName)
        data = f'create {UserName}'
        try:
            self.soc.sendall(data.encode('utf-8'))
            #! momkne error bede 
            window.room_frame.destroy()
            window.chats_frame()
        except socket.error:
            print('Server is down!')

    def client_recv(self):
        while True:
            data = str(self.soc.recv(1024), 'utf-8').split(' ')
            server_method = data[0]
            if server_method == 'create':
                global RoomID
                RoomID = data[1]
            elif server_method == 'message':
                server_message = data[1]
                server_username = data[2]
                server_color = data[3]
                server_roomID = data[4]
                if RoomID != server_roomID :
                    continue
                # Custom tag color
                window.MESSAGEBOX.tag_config(f'{server_username}', foreground=server_color)

                # Insert message
                window.MESSAGEBOX.configure(state='normal')

                #? if username == window.USERNAME.get():
                if server_username == UserName:
                    window.MESSAGEBOX.insert(END, f'Me: {server_message}\n')
                else:
                    window.MESSAGEBOX.insert(INSERT, f'{server_username}: {server_message}\n', f'{server_username}')
                window.MESSAGEBOX.configure(state='disabled')
            




# ------------------------------UI-------------------------------

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser = server(soc)
UserName = ''
RoomID = ''
Color = random_color()


class Window:
    def __init__(self,master:Tk, title,geometery):
        self.master = master
        master.title(title)
        master.geometry(geometery)

        self.IP=StringVar(master)
        self.PORT = StringVar(master)
        self.USERNAME = StringVar(master)
        self.MESSAGE = StringVar(master)

        self.room_frame = Frame(master)
        self.chat_frame = Frame(master)

        self.login_btn= Button(master,text='login',command=self.login)
        self.login_btn.grid(column=2,row=2)

        self.ROOMS_LIST = Listbox(self.room_frame)
        self.MESSAGEBOX = Text(self.chat_frame) 

    def login(self):
        # Login form
        win = Toplevel(self.master)
        win.title('Login')
        win.geometry('200x200')

        # User entry & label
        Label(win, text='Enter your IP').pack()
        Entry(win, textvariable=self.IP).pack()
        Label(win, text='Enter your Port').pack()
        Entry(win, textvariable=self.PORT).pack()
        Label(win, text='Enter your Username').pack()
        Entry(win, textvariable=self.USERNAME).pack()
        Button(win, text='save', command=lambda: check_valid(win, self.IP.get(), self.PORT.get(), self.USERNAME.get())).pack()

    def rooms_frame (self):
        self.login_btn.destroy()

        self.room_frame.pack()

        Label(self.room_frame, text='Avabaile Rooms:').pack()
        self.ROOMS_LIST.pack()
        Entry(self.room_frame).pack()
        Button(self.room_frame,text='Connect').pack()
        Button(self.room_frame,text='Create Room',command=lambda:ser.client_create_room()).pack()
    
    def chats_frame (self):
        self.chat_frame.pack()

        Entry(self.chat_frame,textvariable=self.MESSAGE, width=50).pack()
        self.MESSAGEBOX.pack()
        Button(self.chat_frame,text='Send', command=lambda: ser.client_send(self.MESSAGE.get())).pack()
    
    def insert_listbox(self,num:int):
        for i in range(num):
            self.ROOMS_LIST.insert(i+1,f"Room's {i+1}")




def check_valid(win, IP, PORT, NAME):
    ip_pattern = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", IP)
    name_pattern = re.match(r"[A-Za-z1-9]", NAME)

    if ip_pattern and PORT.isdigit() and name_pattern:
        return ser.connect_to_server(win, IP, int(PORT), NAME)
    else:
        # TODO fix error message
        print('error')
        return False,"That's incorrect"

tk = Tk()
window = Window(tk,"323's Room","400x400")
tk.mainloop()


# ------------------------------Run--------------------------------


