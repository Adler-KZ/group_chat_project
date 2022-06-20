from glob import glob
import threading, socket, random

roomID = 0
clients = []
usernames = []
usernames_roomID = {}


def analyze_data(DATA, CLIENT):
    data = str(DATA, 'utf-8')
    data_items = data.split(' ')
    method = data_items[0]
    global roomID

    if method == 'connect':
        # Unique Username
        username = data_items[1]
        name = username
        while True:
            if name not in usernames:
                break
            name = f'{username}_{random.randint(0, 99)}'
        usernames.append(name)

        data = f'{name} {roomID}'
        CLIENT.sendall(data.encode('utf-8'))

    elif method == 'message':
        for c in clients:
            try:
                c[0].sendall(DATA)
            except:
                print(f'User disconnected')
                clients.remove(c)
    
    elif method == 'create':
        roomID += 1
        username = data_items[1]
        usernames_roomID[username]=roomID

        data = f'create {roomID}'
        CLIENT.sendall(data.encode('utf-8'))


def receive(CLIENT, ADDR):
    while True:
        data = CLIENT.recv(1024)
        analyze_data(data, CLIENT)
        if data == b'':
            print(f'User {ADDR[0]} disconnected')
            break


server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 4000
server_soc.bind((server_ip, server_port))

server_soc.listen(10)
print('server is run')

for i in range(10):
    client, addr = server_soc.accept()
    clients.append((client, addr))
    print(f'The new user ({addr[0]}) joined the server')
    threading.Thread(target=receive, args=(client, addr)).start()

server_soc.close()
