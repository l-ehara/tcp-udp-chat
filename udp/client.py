import socket
import threading

# Server's IP and port
server_ip = '127.0.0.1'
server_port = 55555

# Creating a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set up client's nickname
nickname = input("Choose your nickname: ")
client.sendto(nickname.encode('ascii'), (server_ip, server_port))

def receive():
    while True:
        try:
            data, _ = client.recvfrom(1024)
            print(data.decode('ascii'))
        except:
            print("An error occurred!")
            break

def write():
    print("Type '/pm [nickname] [message]' to send a private message.")
    while True:
        message = input('')
        if message:
            client.sendto(message.encode('ascii'), (server_ip, server_port))

# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()  

write_thread = threading.Thread(target=write)
write_thread.start()
