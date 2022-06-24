from audioop import add
import threading, socket, random,pickle

# ------------------------------Global vaiables-------------------------------
rooms = 0
usernames = []
clients_roomID={}

# ------------------------------Classes-------------------------------
class Data:
    def __init__(self,method='',username='',color='',roomID='',message=''):
        self.method = method
        self.username=username
        self.color=color
        self.roomID = roomID
        self.message = message

class Server:
    def __init__(self,ip='127.0.0.1', port=4000):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.server_soc.bind((ip, port))

    def run(self):
        self.server_soc.listen(10)
        print('server is run')
        for i in range(10):
            client, addr = self.server_soc.accept()
            clients_roomID[(client,addr)]=''
            print(f'The new user ({addr[0]}) joined the server')
            threading.Thread(target=self.receive, args=(client, addr)).start()
        self.server_soc.close()

    def receive(self,CLIENT, ADDR):
        while True:
            try:
                data = CLIENT.recv(1024)
                self.analyze_data(data, CLIENT,ADDR)
            except:
                # TODO age class zadi yadet bashe az list pak koni
                print(f'User {ADDR[0]} disconnected!')
                clients_roomID.pop((CLIENT,ADDR))
                break

    def analyze_data(self,DATA, CLIENT,ADDR):
        data = pickle.loads(DATA)
        global rooms
        match data.method:
            case 'connect':
                # Unique Username
                username = data.username
                name = username
                while True:
                    if name not in usernames:
                        break
                    name = f'{username}_{random.randint(0, 99)}'
                usernames.append(name)
                data = Data(username=name,roomID=rooms)
                CLIENT.sendall(pickle.dumps(data))
            case 'message':
                for c in clients_roomID.keys():
                    if clients_roomID[c]==data.roomID:
                        c[0].sendall(DATA)
                # TODO momkene try except niaz dashte bashe
            case 'create':
                rooms += 1
                clients_roomID[(CLIENT,ADDR)]=str(rooms)
                data = Data(method='create',roomID=str(rooms))
                CLIENT.sendall(pickle.dumps(data))
            case 'exist':
                clients_roomID[(CLIENT,ADDR)] = data.roomID

# ------------------------------Main-------------------------------
if __name__ == '__main__':
    server = Server()
    server.run()
