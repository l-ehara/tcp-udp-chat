import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.2', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break
        
# Sending Messages To Server
def write():
    print("Type '/pm [nickname] [message]' to send a private message.")
    print("Type '/sendtxt [nickname] [filename]' to send a text file.")
    print("Type 'exit' to leave the chat room.")
    print("Type anything else to broadcast your message.")
    while True:
        message = input('')
        if message.startswith('/sendtxt'):
            try:
                _, recipient_nickname, filename = message.split(' ', 2)
                with open(filename, 'r') as file:
                    contents = file.read()
                file_message = f'/sendtxt {recipient_nickname} {contents}'
                client.send(file_message.encode('ascii'))
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()