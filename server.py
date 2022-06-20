import threading, socket, random

clients = []
usernames_colors = {}
room__id = 1


def analyze_data(DATA, CLIENT):
    data = str(DATA, 'utf-8')
    data_items = data.split(' ')
    method = data_items[0]

    if method == 'connect':
        username = data_items[1]
        color = data_items[2]
        # Unique Username
        while True:
            name = f'{username}_{random.randint(0, 99)}'
            if name not in usernames_colors.keys():
                break
        # Append to list
        usernames_colors[name] = color
        CLIENT.sendall(name.encode('utf-8'))

    elif method == 'message':
        for c in clients:
            try:
                c[0].sendall(DATA)
            except:
                print(f'User disconnected')
                clients.remove(c)



def receive(CLIENT, ADDR):
    while True:
        data = CLIENT.recv(1024)
        analyze_data(data, CLIENT)
        # username = CLIENT.recv(1024)
        # for c in clients:
        #     try:
        #         c[0].sendall(data)
        #         c[0].sendall(username)
        #     except:
        #         print(f'User {ADDR[0]} disconnected')
        #         clients.remove(c)
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
