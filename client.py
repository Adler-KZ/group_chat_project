
import socket,threading,re,random,pickle
from tkinter import *
from tkinter import messagebox
from server import Data

# ------------------------------Functions-------------------------------

# <-------Check True Validation------->
def check_valid(SERVER, ip, port, username):
    ipP = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    usernameP = re.match(r"[A-Za-z]+", username)

    if ipP and port.isdigit():
        if usernameP:
            return SERVER.connect_to_server(ip, int(port), username)
        else:
            messagebox.showerror('Error','Your username is not Valid!\nPlease change it')
    else:
        messagebox.showerror('Error','This IP & port are incorrect\nPlease fix it')

# <-------Unique Color------->
def random_color():
    R = random.randint(30, 150)
    G = random.randint(30, 150)
    B = random.randint(30, 150)
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
            data = Data('connect',NAME)
            self.soc.sendall(pickle.dumps(data))
            response = pickle.loads(self.soc.recv(1024))
            self.UserName = response.username
            self.window.insert_listbox(response.roomID)
            self.window.room_frame()
            threading.Thread(target=self.client_recv).start()
        except socket.error:
            messagebox.showwarning('404','Server Not Found!')

    def client_send(self,method, msg=''):
        match method:
            case 'message':
                data = Data(method,self.UserName,self.Color,self.RoomID,msg)
            case 'create':
                data = Data(method,username=self.UserName)
            case 'exist':
                data = Data(method,roomID=self.RoomID,username=self.UserName)
        try:
            self.soc.sendall(pickle.dumps(data))
            if method == 'create' : self.window.chat_window() 
        except socket.error:
            if messagebox.showerror('Sorry','Server is down!'):
                quit()

    def client_recv(self):
        while True:
            try:
                data = pickle.loads(self.soc.recv(1024))
                match data.method :
                    case 'create':
                        self.RoomID = data.roomID
                    case 'message':
                        try:
                            # Custom tag color for print with diffrent color
                            self.window.MESSAGEBOX.tag_config(f'{data.username}', foreground=data.color)
                            # Insert message in messagebox 
                            self.window.MESSAGEBOX.configure(state='normal')
                            if data.username == self.UserName:
                                self.window.MESSAGEBOX.insert(END, f'Me: {data.message}\n')
                            else:
                                self.window.MESSAGEBOX.insert(INSERT, f'{data.username} :  {data.message}\n', f'{data.username}')
                            self.window.MESSAGEBOX.configure(state='disabled')
                        except:
                            pass
                    case 'update':
                        # Update Avabaile Rooms when user create a new room
                        if data.roomID:
                            self.window.insert_listbox(data.roomID)
                        # Update the users in a same room
                        self.window.onlineT.configure(state='normal')
                        self.window.onlineT.delete("1.0","end")
                        for roomID,username in data.list:
                            if roomID == self.RoomID:
                                self.window.onlineT.tag_configure("tag_name", justify='center')
                                self.window.onlineT.insert(END,f'{username}\n')
                                self.window.onlineT.tag_add("tag_name", "1.0", "end")
                        self.window.onlineT.configure(state='disabled')
            except ConnectionResetError:
                break
            except AttributeError:
                continue
            
# <-------Window Class------->
class Window:
    def __init__(self,server:Server,master:Tk, title:str,geometery:str):
        self.server=server
        # Main window attr
        self.master = master
        self.master.title(title)
        self.master.geometry(geometery)
        self.master.protocol('WM_DELETE_WINDOW',self.main_exit)
        self.master.resizable(0,0)
        # Variables
        self.IP=StringVar(master)
        self.PORT = StringVar(master)
        self.USERNAME = StringVar(master)
        self.MESSAGE = StringVar(master)
        # Frames
        self.mainF = Frame(master)
        self.roomF = Frame(master)
        # Listbox room & dounble click event
        self.ROOMS_LIST = Listbox(self.roomF,font=('calibri',13))
        self.ROOMS_LIST.bind('<Double-1>', self.double_click_event)
        # Run main frame
        self.main_frame()

    def main_frame(self):
        self.mainF.pack(fill='both',expand=True)
        self.mainF.config(bg='#cf91ff')
        # widget
        nameL = Label(self.mainF,text='ROOM 323',bg ='#cf91ff',font=('impact',40))
        welcomeL = Label(self.mainF,text='Welcome to the',bg ='#cf91ff',font=('franklin fothic',30))
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
        ipE=Entry(self.loginF, textvariable=self.IP,font=('corbel',10))
        ipL = Label(self.loginF, text='Enter your IP :',font=('arial',10))
        portE=Entry(self.loginF, textvariable=self.PORT,font=('corbel',10))
        portL = Label(self.loginF, text='Enter your Port :',font=('arial',10))
        usernameE=Entry(self.loginF, textvariable=self.USERNAME,font=('corbel',10))
        usernameL = Label(self.loginF, text='Enter your Username :',font=('arial',10))
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

    def room_frame (self):
        self.loginF.destroy()
        self.mainF.destroy()
        self.roomF.pack(fill='both',expand=True)
        self.roomF.config(bg='#cf91ff')
        # Widgets
        createB = Button(self.roomF,text='Create Room',command=lambda:self.server.client_send('create'),font=('arial',12))
        usernameL = Label(self.roomF, text=f'welcome {self.server.UserName}',font=('gabriola',35),bg='#cf91ff')
        roomsL = Label(self.roomF, text='Avabaile Rooms:',font=('arial',12),bg='#cf91ff')
        # Show Widgets
        usernameL.pack(pady=5)
        roomsL.pack(padx=(0,220),side=TOP)
        self.ROOMS_LIST.pack(expand=True,fill='both',padx=25,pady=(2,5))
        createB.pack(pady=(0,2),ipadx=5)
        
    def chat_window (self):
        self.master.withdraw()
        # Chat Window attr
        self.chatW = Toplevel(self.master)
        self.chatW.protocol('WM_DELETE_WINDOW',self.chat_exit)
        self.chatW.resizable(0,0)
        # Widgets
        usernameL = Label(self.chatW, text=f'{self.server.UserName} ',font=('century gothic',15),bg='white')
        messageE = Entry(self.chatW,textvariable=self.MESSAGE, width=50,font=('century',15))
        messageE.bind('<Return>',self.send_btn_event)
        sendB = Button(self.chatW,text='Send', command=self.send_btn_event,font=('corbel',12),bg='#32a850')
        # Globals widgets
        self.onlineT = Text(self.chatW,font=('century',13),width=15) 
        self.MESSAGEBOX = Text(self.chatW,bg='#d3d3d3',font=('century',12),width=25) 
        self.MESSAGEBOX.configure(state='disabled')
        # Show Widgets
        self.onlineT.pack(side=RIGHT,expand=True,fill='both')
        self.MESSAGEBOX.pack(side= TOP,fill='both', expand=True)
        usernameL.pack(side=LEFT,fill='both')
        messageE.pack(side=LEFT,expand=True,fill='both')
        sendB.pack(side=RIGHT,fill='both',ipadx=10)
        
    def insert_listbox(self,num:int):
        try:
            self.ROOMS_LIST.delete(0,'end')
            for i in range(num):
                self.ROOMS_LIST.insert(i+1,f"Room {i+1}")
        except:
            pass

    # Events
    def double_click_event(self, event):
        self.chat_window()
        selected_room = self.ROOMS_LIST.curselection()
        self.server.RoomID = selected_room[0]+1
        self.server.client_send('exist')       

    def login_btn_event(self,event=None):
        check_valid(self.server ,self.IP.get(), self.PORT.get(), self.USERNAME.get())

    def send_btn_event(self,event=None):
        message = self.MESSAGE.get()
        if bool(message):
            self.server.client_send('message',self.MESSAGE.get())
            self.MESSAGE.set('')

    # Exit button defines
    def main_exit(self):
        self.server.soc.close()
        self.master.destroy()
        quit()

    def chat_exit(self):
        if messagebox.askyesno('','Do you want to close the program?\nOr want to change room?'):
            self.server.soc.close()
            self.chatW.destroy()
            self.master.destroy()
            quit()
        else:
            self.chatW.destroy()
            self.master.deiconify()

# ------------------------------Main-------------------------------

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tk = Tk()
server = Server(soc)
win = Window(server,tk,"Room 323","400x400")
server.window = win
tk.mainloop()
