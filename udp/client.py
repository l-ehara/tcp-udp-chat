import socket
import threading
import os
import base64

defaultpath = "./udp/"
server_ip = "127.0.0.5"
server_port = 55555
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nickname = input("Choose your nickname: ")
client.sendto(nickname.encode("ascii"), (server_ip, server_port))

def send_file_in_chunks(filepath, recipient_nickname, chunk_size=508):
    with open(filepath, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break  # File transmission is done
            encoded_chunk = base64.b64encode(chunk)
            client.sendto(f"/filedata {recipient_nickname} {encoded_chunk.decode('ascii')}".encode('ascii'), (server_ip, server_port))
        client.sendto(f"/endfile {recipient_nickname}".encode('ascii'), (server_ip, server_port))

def receive():
    while True:
        try:
            data, _ = client.recvfrom(1024)
            print(data.decode("ascii"))
        except:
            print("An error occurred!")
            break

def write():
    print("Type '/pm [nickname] [message]' to send a private message.")
    print("Type '/sendtxt [nickname] [filename]' to send a text file content.")
    print("Type '/sendfile [nickname] [filename]' to send a text file.")
    print("Type '/exit' to leave the chat room.")
    print("Type anything else to broadcast your message.")
    while True:
        message = input("")
        if message.startswith("/sendfile"):
            _, recipient_nickname, filename = message.split(" ", 2)
            fullpath = os.path.join(defaultpath, filename)
            if os.path.isfile(fullpath):
                client.sendto(f"/sendfile {recipient_nickname} {filename}".encode("ascii"), (server_ip, server_port))
                send_file_in_chunks(fullpath, recipient_nickname)
            else:
                print("File not found. Please check the filename and try again.")
        else:
            client.sendto(message.encode("ascii"), (server_ip, server_port))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
