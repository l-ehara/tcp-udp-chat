# TCP/UDP Chat Application

## Introduction
This repository contains a simple chat application implemented in Python that demonstrates the use of both TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) for network communication. The application includes separate server and client scripts for each protocol, allowing users to explore the differences in how TCP and UDP handle data transmission.

## Getting Started

### Prerequisites
- Python 3.x
- Access to a command-line interface

### Running the Application

*Note*: **ALWAYS RUN THE SERVER FIRST!**

#### TCP Chat
1. **Start the TCP Server:**
   - Navigate to the `tcp` directory.
   - Run the server script using Python:
     ```bash
     python3 server.py
     ```
2. **Run the TCP Client:**
   - Open a new command-line interface window.
   - Navigate to the `tcp` directory.
   - Start the client script:
     ```bash
     python3 client.py
     ```

#### UDP Chat
1. **Start the UDP Server:**
   - Navigate to the `udp` directory.
   - Run the server script:
     ```bash
     python3 server.py
     ```
2. **Run the UDP Client:**
   - Open a new command-line interface window.
   - Navigate to the `udp` directory.
   - Start the client script:
     ```bash
     python3 client.py
     ```

## Features

1. **Broadcast a message:** 
    - Using a client, type anything and the message is going to be broadcasted.
2. **Send a Private Message:** 
    - Using a client, type: 
        ```bash 
        /pm [nickname] [message]
        ``` 
3. **Send a .txt content to another client:**   
    - Using a client, type:
        ```bash 
        /sendtxt [nickname] [filename]
        ``` 
    - *Note*: _The file has to be into the **tcp/** or **udp/** folder depending on which you are using. There is already a testfile(TCP/UDP).txt to facilitate the usage_
4. **Send a .txt file to another client:**   
    - Using a client, type:
        ```bash 
        /sendtxt [nickname] [filename]
        ``` 
    - *Note*: _The file has to be into the **tcp/** or **udp/** folder depending on which you are using. There is already a testfile(TCP/UDP).txt to facilitate the usage_
5. **Exit with a client:** 
    - Using a client, type:
        ```bash 
        /exit
        ```

## Understanding TCP and UDP
 - TCP is a connection-oriented protocol, ensuring that all packets arrive at their destination in the same order they were sent. This is ideal for applications where accuracy is critical, such as web browsing and email.

 - UDP is a connectionless protocol, which does not guarantee packet order or delivery. This makes UDP faster and more efficient for applications where speed is more important than precision, such as streaming audio and video.

## Conclusion
This chat application provides a basic framework for understanding and experimenting with TCP and UDP protocols. You can extend the functionality or adapt the code for different network communication scenarios.

