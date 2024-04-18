import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# BROADCAST A MESSAGE
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            server.sendto(message, client)

# Handling Messages From Clients
def handle():
    while True:
        try:
            message, client_address = server.recvfrom(1024)
            message = message.decode('ascii')
            if client_address not in clients:
                # This is a new client, store their nickname
                nicknames.append(message)
                clients.append(client_address)
                broadcast(f"{message} joined!".encode('ascii'))
                print(f"Connected with {client_address} with nickname {message}")
                continue

            if message.startswith('/pm'):
                _, recipient_nickname, private_message = message.split(' ', 2)
                if recipient_nickname in nicknames:
                    recipient_index = nicknames.index(recipient_nickname)
                    recipient_client = clients[recipient_index]
                    sender_index = clients.index(client_address)
                    sender_nickname = nicknames[sender_index]
                    server.sendto(f'PM from {sender_nickname}: {private_message}'.encode('ascii'), recipient_client)
                else:
                    server.sendto(f'{recipient_nickname} is not online.'.encode('ascii'), client_address)
            elif message == '/exit':
                index = clients.index(client_address)
                nickname = nicknames[index]
                broadcast(f'{nickname} left!'.encode('ascii'), sender=client_address)
                clients.remove(client_address)
                nicknames.remove(nickname)
            else:
                index = clients.index(client_address)
                sender_nickname = nicknames[index]
                broadcast_message = f'{sender_nickname}: {message}'.encode('ascii')
                broadcast(broadcast_message, sender=client_address)
        except Exception as e:
            print(f"An error occurred: {e}")

# Start the handling thread
thread = threading.Thread(target=handle)
thread.start()
