
from cmath import exp
import socket
import threading
import re
import random
from tkinter import *
from tkinter import messagebox


# ------------------------------Functions-------------------------------

# <-------Check True Validation------->
def check_valid(SERVER, ip, port, username):
    ipP = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    usernameP = re.match(r"[A-Za-z1-9]", username)

    if ipP and usernameP and port.isdigit():
        return SERVER.connect_to_server(ip, int(port), username)
    else:
        print('error')
        messagebox.showerror('Not Valid Format!','This data is not standard!')

# <-------Unique Color------->
def random_color():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    hex_color = "#{:02x}{:02x}{:02x}".format(R, G, B)
    return hex_color


# ------------------------------Classes-------------------------------

# <-------Server Class------->
class Server:
    def __init__(self, soc:socket.socket, window=None):
        self.soc = soc
        self.window=window
        self.RoomID = ''
        self.UserName = ''
        self.Color = random_color()

    def connect_to_server(self, IP: str, PORT: int, NAME: str):
        try:
            self.soc.connect((IP, PORT))
            # Send username and get response from server
            data = f'connect {NAME}'.encode('utf-8')
            self.soc.sendall(data)
            response = str(self.soc.recv(1024), 'utf-8').split(' ')
            self.UserName = response[0]
            self.window.insert_listbox(int(response[1]))
            self.window.rooms_frame()
            threading.Thread(target=self.client_recv).start()
        except:
            messagebox.showwarning('404','Server Not Found!')


    def client_send_message(self, msg):
        data = f'message {msg} {self.UserName} {self.Color} {self.RoomID}'
        try:
            self.soc.sendall(data.encode('utf-8'))
        except socket.error:
            if messagebox.showerror('Sorry','Server is down!'):
                quit()
    
    def client_create_room(self):
        data = f'create {self.UserName}'
        try:
            self.soc.sendall(data.encode('utf-8'))
            self.window.chats_frame()
        except socket.error:
            if messagebox.showerror('Sorry','Server is down!'):
                quit()

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
        self.master.title(title)
        self.master.geometry(geometery)
        self.master.protocol('WM_DELETE_WINDOW',self.EXIT)
        self.master.resizable(0,0)
        # Variables
        self.IP=StringVar(master)
        self.PORT = StringVar(master)
        self.USERNAME = StringVar(master)
        self.MESSAGE = StringVar(master)
        # Frames
        self.mainF = Frame(master)
        self.roomF = Frame(master)
        self.chatF = Frame(master)
        # Listbox room & dounble click event
        self.ROOMS_LIST = Listbox(self.roomF,font=('calibri',13))
        self.ROOMS_LIST.bind('<Double-1>',self.double_ckick_event)
        # Run main frame
        self.main_frame()

    def main_frame(self):
        self.mainF.pack(fill='both',expand=True)
        self.mainF.config(bg='#cf91ff')
        # widget
        welcomeL = Label(self.mainF,text='Welcome to the',bg ='#cf91ff',font=('franklin fothic',30))
        nameL = Label(self.mainF,text='ROOM 323',bg ='#cf91ff',font=('impact',40))
        loginB = Button(self.mainF,text='Login',command=self.login_window,font=('impact',18,'italic'),bg='#237ca6')
        # Show Widgets
        welcomeL.pack(pady=(50,0))
        nameL.pack(pady=(0,55))
        loginB.pack(pady=50)

    def login_window(self):
        # login window attr
        self.loginF = Toplevel(self.master)
        self.loginF.title('Login')
        self.loginF.geometry('300x180')
        self.loginF.resizable(0,0)
        # Widgets
        ipL = Label(self.loginF, text='Enter your IP :',font=('arial',10))
        portL = Label(self.loginF, text='Enter your Port :',font=('arial',10))
        usernameL = Label(self.loginF, text='Enter your Username :',font=('arial',10))
        ipE=Entry(self.loginF, textvariable=self.IP,font=('corbel',10))
        portE=Entry(self.loginF, textvariable=self.PORT,font=('corbel',10))
        usernameE=Entry(self.loginF, textvariable=self.USERNAME,font=('corbel',10))
        loginB = Button(self.loginF, text='Login',command=self.login_btn_event,font=('corbel',10))
        loginB.bind('<Return>',self.login_btn_event)
        # Show Widgets
        ipL.grid(row=0,column=2,pady=10,padx=(7,1))
        ipE.grid(row=0,column=3,pady=10)
        portL.grid(row=1,column=2,pady=10,padx=(7,1))
        portE.grid(row=1,column=3,pady=10)
        usernameL.grid(row=2,column=2,pady=10,padx=(7,1))
        usernameE.grid(row=2,column=3,pady=10)
        loginB.grid(row=3,column=2,columnspan=2,pady=10)

    def rooms_frame (self):
        self.loginF.destroy()
        self.mainF.destroy()
        self.roomF.pack(fill='both',expand=True)
        self.roomF.config(bg='#cf91ff')
        # Widgets
        usernameL = Label(self.roomF, text=f'Wellcome {self.server.UserName}',font=('gabriola',35),bg='#cf91ff')
        roomsL = Label(self.roomF, text='Avabaile Rooms:',font=('arial',12),bg='#cf91ff')
        createB = Button(self.roomF,text='Create Room',command=lambda:self.server.client_create_room(),font=('arial',12))
        # Show Widgets
        usernameL.pack(pady=5)
        roomsL.pack(padx=(0,220),side=TOP)
        self.ROOMS_LIST.pack(expand=True,fill='both',padx=25,pady=(2,5))
        createB.pack(pady=(0,2),ipadx=5)
        
    
    def chats_frame (self):
        self.roomF.destroy()
        self.chatF.pack()
        self.master.geometry('')
        self.master.resizable(0,0)
        #widget
        usernameL = Label(self.chatF, text=f'{self.server.UserName} ',font=('century gothic',15),bg='white')
        messageE = Entry(self.chatF,textvariable=self.MESSAGE, width=50,font=('century',15))
        messageE.bind('<Return>',self.send_btn_event)
        sendB = Button(self.chatF,text='Send', command=self.send_btn_event,font=('corbel',12),bg='#32a850')
        self.MESSAGEBOX = Text(self.chatF,bg='#d3d3d3',font=('century',12)) 
        # Show Widgets
        self.MESSAGEBOX.pack(side= TOP,fill='both', expand=True)
        usernameL.pack(side=LEFT,fill='both')
        messageE.pack(side=LEFT,expand=True,fill='both')
        sendB.pack(side=RIGHT,fill='both',ipadx=10)
    
    def insert_listbox(self,num:int):
        for i in range(num):
            self.ROOMS_LIST.insert(i+1,f"Room {i+1}")
    
    # Events
    def double_ckick_event(self,event):
        selected_room = self.ROOMS_LIST.curselection()
        self.server.RoomID = str(selected_room[0]+1)       
        self.chats_frame()
    def login_btn_event(self,event=None):
        check_valid(self.server ,self.IP.get(), self.PORT.get(), self.USERNAME.get())
    def send_btn_event(self,event=None):
        message = self.MESSAGE.get()
        if bool(message):
            self.server.client_send_message(self.MESSAGE.get())
            self.MESSAGE.set('')

    def EXIT(self):
        self.server.soc.close()
        self.master.destroy()


# ------------------------------Main-------------------------------

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tk = Tk()
server = Server(soc)
win = Window(server,tk,"Room 323","400x400")
server.window = win
tk.mainloop()
