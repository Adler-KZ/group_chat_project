import threading, socket, random,pickle

# ------------------------------Global vaiables-------------------------------
rooms = 0
usernames=[]
clients_RoomUser={}

# ------------------------------Classes-------------------------------
class Data:
    def __init__(self,method='',username='',color='',roomID='',message='',list=''):
        self.method = method
        self.username=username
        self.color=color
        self.roomID = roomID
        self.message = message
        self.list = list

class Server:
    def __init__(self,ip='127.0.0.1', port=4000):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.server_soc.bind((ip, port))

    def run(self):
        self.server_soc.listen(30)
        print('Server is running...')
        for i in range(30):
            client, addr = self.server_soc.accept()
            clients_RoomUser[(client,addr)]=''
            print(f'The new user ({addr[0]}) joined the server')
            threading.Thread(target=self.receive, args=(client, addr)).start()
        self.server_soc.close()

    def receive(self,CLIENT, ADDR):
        while True:
            try:
                data = CLIENT.recv(1024)
                self.analyze_data(data, CLIENT,ADDR)
            except:
                roomID, user = clients_RoomUser.pop((CLIENT, ADDR))
                print(f'User ({user}) in Room ({roomID}) disconnected!')
                usernames.remove(user)
                self.users_in_room()
                break

    def analyze_data(self,DATA, CLIENT,ADDR):
        data = pickle.loads(DATA)
        global rooms
        match data.method:
            #* Client wants to connect the server
            case 'connect':
                # Unique Username
                name = data.username
                while True:
                    if name not in usernames:
                        break
                    name = f'{data.username}_{random.randint(0, 99)}'
                # Save Username
                usernames.append(name)
                clients_RoomUser[(CLIENT,ADDR)]=('Unknown',name)
                # Send new username to client
                data = Data(username=name,roomID=rooms)
                CLIENT.sendall(pickle.dumps(data))
            #* Server receive message from a client then sends to the all clients that are in a same room
            case 'message':
                for c in clients_RoomUser.keys():
                    if clients_RoomUser[c][0]==data.roomID:
                        c[0].sendall(DATA)
            #* Client wants to the create a new room
            case 'create':
                rooms += 1
                clients_RoomUser[(CLIENT,ADDR)]=(rooms,data.username)
                data = Data(method='create',roomID=rooms)
                CLIENT.sendall(pickle.dumps(data))
                self.users_in_room()
            #* Client wants to join an exist room
            case 'exist':
                clients_RoomUser[(CLIENT,ADDR)] = (data.roomID,data.username)
                self.users_in_room()
    
    def users_in_room(self):
        data = Data(method='refresh',list = list(clients_RoomUser.values()))
        for c in clients_RoomUser.keys():
            c[0].sendall(pickle.dumps(data))

# ------------------------------Main-------------------------------
if __name__ == '__main__':
    server = Server()
    server.run()
