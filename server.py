from __future__ import barry_as_FLUFL
import threading, socket, random

# Global vaiables
rooms = 0
clients = []
usernames = []
usernames_roomID = {}

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
            clients.append((client, addr))
            print(f'The new user ({addr[0]}) joined the server')
            threading.Thread(target=self.receive, args=(client, addr)).start()
        self.server_soc.close()

    def receive(self,CLIENT, ADDR):
        while True:
            try:
                data = CLIENT.recv(1024)
                self.analyze_data(data, CLIENT)
            except ConnectionResetError:
                # TODO age class zadi yadet bashe az list pak koni
                print('user disconnected')
                clients.remove((CLIENT,ADDR))
                break


    def analyze_data(self,DATA, CLIENT):
        data = str(DATA, 'utf-8')
        data_items = data.split(' ')
        method = data_items[0]
        global rooms

        if method == 'connect':
            # Unique Username
            username = data_items[1]
            name = username
            while True:
                if name not in usernames:
                    break
                name = f'{username}_{random.randint(0, 99)}'
            usernames.append(name)

            data = f'{name} {rooms}'
            CLIENT.sendall(data.encode('utf-8'))

        elif method == 'message':
            for c in clients:
                c[0].sendall(DATA)
            # for c in clients:
            #     try:
            #         c[0].sendall(DATA)
            #     except:
            #         print(f'User disconnected')
            #         clients.remove(c)
        
        elif method == 'create':
            rooms += 1
            username = data_items[1]
            usernames_roomID[username]=rooms

            data = f'create {rooms}'
            CLIENT.sendall(data.encode('utf-8'))

server = Server()
server.run()
# server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_ip = '127.0.0.1'
# server_port = 4000
# server_soc.bind((server_ip, server_port))

# server_soc.listen(10)
# print('server is run')

# for i in range(10):
#     client, addr = server_soc.accept()
#     clients.append((client, addr))
#     print(f'The new user ({addr[0]}) joined the server')
#     threading.Thread(target=receive, args=(client, addr)).start()

# server_soc.close()
