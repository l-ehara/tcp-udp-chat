import socket
import threading
import os

defaultpath = "./tcp/"

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
    print("Type '/sendtxt [nickname] [filename]' to send a text file.")
    print("Type '/exit' to leave the chat room.")
    print("Type anything else to broadcast your message.")
    while True:
        message = input('')
        if message.startswith('/sendtxt'):
            try:
                _, recipient_nickname, filename = message.split(' ', 2)
                fullpath = os.path.join(defaultpath, filename)
                with open(fullpath, 'r') as file:
                    contents = file.read()
                file_message = f'/sendtxt {recipient_nickname} {contents}'
                client.sendto(file_message.encode('ascii'), (server_ip, server_port))
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message:
            client.sendto(message.encode('ascii'), (server_ip, server_port))


# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()  

write_thread = threading.Thread(target=write)
write_thread.start()
