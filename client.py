import socket
import threading
import re
import random
from tkinter import *

UserName = ''
Room = ''
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
    def __init__(self, soc):
        self.soc = soc

    def connect_to_server(self,win, IP: str, PORT: int, NAME: str):
        try:
            self.soc.connect((IP, PORT))
            # Send username and get response from server
            data = f'connect {NAME} {Color}'.encode('utf-8')
            print(data)
            self.soc.sendall(data)
            response = str(self.soc.recv(1024), 'utf-8')
            UserName = response

            window.rooms_frame()
            win.destroy()
            threading.Thread(target=self.client_recv).start()
        except:
            print('Something is wrong!')
            win.destroy()

    def client_send(self, msg):
        data = f'message {msg} {UserName} {Color}'
        # data = self.pack_data('message',msg,name,color)
        try:
            self.soc.sendall(data.encode('utf-8'))
        except socket.error:
            print('Server is down!')

    def client_recv(self):
        while True:
            data = str(self.soc.recv(1024), 'utf-8').split(' ')
            message = data[1]
            username = data[2]

            # Custom tag color
            color = data[3]
            window.MESSAGEBOX.tag_config(f'{username}', foreground=color)

            # Insert message
            window.MESSAGEBOX.configure(state='normal')
            if username == window.USERNAME.get():
                window.MESSAGEBOX.insert(END, f'Me: {message}\n')
            else:
                window.MESSAGEBOX.insert(INSERT, f'{username}: {message}\n', f'{username}')
            window.MESSAGEBOX.configure(state='disabled')




# ------------------------------UI-------------------------------

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser = server(soc)
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
        Listbox(self.room_frame).pack()
        Entry(self.room_frame).pack()
        Button(self.room_frame,text='Connect').pack()
        Button(self.room_frame,text='Create Room').pack()
    
    def chats_frame (self):
        self.chat_frame.pack()

        Entry(self.chat_frame,textvariable=self.MESSAGE, width=50).pack()
        self.MESSAGEBOX.pack()
        Button(self.chat_frame,text='Send', command=lambda: ser.client_send(self.MESSAGE.get()))




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


