import socket
import threading
import os
import base64

nickname = input("Choose your nickname: ")
defaultpath = "./tcp/"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.2", 55555))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except Exception as e:
            print("An error occurred!", e)
            client.close()
            break


def write():
    print(
        "Commands:\n'/pm [nickname] [message]'\n'/sendtxt [nickname] [filename]'\n'/sendfile [nickname] [filename]'\n'/exit'"
    )
    while True:
        message = input("")
        if message.startswith("/sendfile"):
            _, recipient_nickname, filename = message.split(" ", 2)
            fullpath = os.path.join(defaultpath, filename)
            try:
                with open(fullpath, "rb") as file:
                    file_data = file.read()
                    encoded_data = base64.b64encode(file_data)
                    header = f"/sendfile {recipient_nickname} {filename}"
                    client.send(header.encode("ascii"))
                    client.send(encoded_data) 
                    client.send(b"EOF")
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message.startswith("/sendtxt"):
            try:
                _, recipient_nickname, filename = message.split(" ", 2)
                fullpath = os.path.join(defaultpath, filename)
                with open(fullpath, "r") as file:
                    contents = file.read()
                file_message = f"/sendtxt {recipient_nickname} {contents}"
                client.send(file_message.encode("ascii"))
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message:
            client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)
receive_thread.start()
write_thread.start()
