import socket 
import threading

# Connection Data
host = '127.0.0.2'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# BROADCAST A MESSAGE
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith('/pm'):
                _, recipient_nickname, private_message = message.split(' ', 2)
                handle_pm(client, recipient_nickname, private_message)
            elif message.startswith('/sendtxt'):
                _, recipient_nickname, file_contents = message.split(' ', 2)
                handle_sendtxt(client, recipient_nickname, file_contents)
            elif message == 'exit':
                handle_exit(client)
            else:
                handle_broadcast(client, message)
        except Exception as e:
            handle_disconnect(client)

def handle_pm(client, recipient_nickname, message):
    if recipient_nickname in nicknames:
        recipient_index = nicknames.index(recipient_nickname)
        recipient_client = clients[recipient_index]
        sender_index = clients.index(client)
        sender_nickname = nicknames[sender_index]
        recipient_client.send(f'PM from {sender_nickname}: {message}'.encode('ascii'))
    else:
        client.send(f'{recipient_nickname} is not online.'.encode('ascii'))

def handle_sendtxt(client, recipient_nickname, file_contents):
    if recipient_nickname in nicknames:
        recipient_index = nicknames.index(recipient_nickname)
        recipient_client = clients[recipient_index]
        sender_index = clients.index(client)
        sender_nickname = nicknames[sender_index]
        recipient_client.send(f'File from {sender_nickname}: {file_contents}'.encode('ascii'))
    else:
        client.send(f'{recipient_nickname} is not online.'.encode('ascii'))

def handle_broadcast(client, message):
    index = clients.index(client)
    sender_nickname = nicknames[index]
    broadcast_message = f'{sender_nickname}: {message}'
    broadcast(broadcast_message.encode('ascii'))

def handle_exit(client):
    broadcast(f'{nicknames[clients.index(client)]} left the chat.'.encode('ascii'))
    client.close()

def handle_disconnect(client):
    index = clients.index(client)
    nickname = nicknames[index]
    broadcast(f'{nickname} left!'.encode('ascii'))
    clients.remove(client)
    nicknames.remove(nickname)
    client.close()



#What it then does is receiving the message from the client 
#(if he sends any) and broadcasting it to all connected clients. 
#So when one client sends a message, everyone else can see this message.
#Now if for some reason there is an error with the connection to this client,
#we remove it and its nickname, close the connection and broadcast that this 
#client has left the chat. After that we break the loop and this thread comes 
#to an end. Quite simple. We are almost done with the server but we need one final function.


# Receiving Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()