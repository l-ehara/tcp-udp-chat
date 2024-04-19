import socket
import threading
import os
import base64

# Connection Data
host = "127.0.0.1"
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


def broadcast(message, sender=None):
    for client in clients:
        server.sendto(message, client)


def handle_sendfile(
    sender_nickname, recipient_nickname, filename, encoded_file_data, sender_address
):
    if recipient_nickname in nicknames:
        recipient_index = nicknames.index(recipient_nickname)
        recipient_client = clients[recipient_index]
        file_data = base64.b64decode(encoded_file_data.encode("ascii"))

        recipient_dir = f"./udp_inbox/{recipient_nickname}/"
        if not os.path.exists(recipient_dir):
            os.makedirs(recipient_dir)
        file_path = os.path.join(recipient_dir, filename)
        with open(file_path, "wb") as file:
            file.write(file_data)

        server.sendto(
            f"File {filename} from {sender_nickname} successfully received and saved.".encode(
                "ascii"
            ),
            recipient_client,
        )
    else:
        server.sendto(
            f"{recipient_nickname} is not online.".encode("ascii"), sender_address
        )


def handle_pm(sender_nickname, recipient_nickname, private_message, sender_address):
    if recipient_nickname in nicknames:
        recipient_index = nicknames.index(recipient_nickname)
        recipient_client = clients[recipient_index]
        server.sendto(
            f"PM from {sender_nickname}: {private_message}".encode("ascii"),
            recipient_client,
        )
    else:
        server.sendto(
            f"{recipient_nickname} is not online.".encode("ascii"), sender_address
        )


def handle_sendtxt(sender_nickname, recipient_nickname, file_contents, sender_address):
    if recipient_nickname in nicknames:
        recipient_index = nicknames.index(recipient_nickname)
        recipient_client = clients[recipient_index]
        server.sendto(
            f"File from {sender_nickname}: {file_contents}".encode("ascii"),
            recipient_client,
        )
    else:
        server.sendto(
            f"{recipient_nickname} is not online.".encode("ascii"), sender_address
        )


def handle_exit(nickname, sender_address):
    index = clients.index(sender_address)
    broadcast(f"{nickname} left!".encode("ascii"), sender=sender_address)
    clients.remove(sender_address)
    nicknames.remove(nickname)


def handle():
    while True:
        try:
            message, client_address = server.recvfrom(1024)
            message = message.decode("ascii")
            if client_address not in clients:
                nicknames.append(message)
                clients.append(client_address)
                broadcast(f"{message} joined!".encode("ascii"))
                print(f"Connected with {client_address} with nickname {message}")
                continue
            if message.startswith("/pm"):
                _, recipient_nickname, private_message = message.split(" ", 2)
                sender_index = clients.index(client_address)
                sender_nickname = nicknames[sender_index]
                handle_pm(
                    sender_nickname, recipient_nickname, private_message, client_address
                )
            elif message.startswith("/sendtxt"):
                _, recipient_nickname, file_contents = message.split(" ", 2)
                sender_index = clients.index(client_address)
                sender_nickname = nicknames[sender_index]
                handle_sendtxt(
                    sender_nickname, recipient_nickname, file_contents, client_address
                )
            elif message.startswith("/sendfile"):
                _, recipient_nickname, filename, encoded_file_data = message.split(
                    " ", 3
                )
                sender_index = clients.index(client_address)
                sender_nickname = nicknames[sender_index]
                handle_sendfile(
                    sender_nickname,
                    recipient_nickname,
                    filename,
                    encoded_file_data,
                    client_address,
                )
            elif message == "/exit":
                index = clients.index(client_address)
                nickname = nicknames[index]
                handle_exit(nickname, client_address)
            else:
                index = clients.index(client_address)
                sender_nickname = nicknames[index]
                broadcast_message = f"{sender_nickname}: {message}".encode("ascii")
                broadcast(broadcast_message, sender=client_address)
        except Exception as e:
            print(f"An error occurred: {e}")


# Start the handling thread
thread = threading.Thread(target=handle)
thread.start()
