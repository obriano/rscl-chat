import socket
import threading


HOST = '10.0.2.15'
PORT = 1776

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
public_keys = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            #print(f"{message.decode('utf-8')}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f"Server: {nickname} has disconnected.")
            broadcast(f'Server: {nickname} has left the chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Server: Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname_and_key = client.recv(1024).decode('utf-8').split(':')
        nickname = nickname_and_key[0]
        public_key = nickname_and_key[1]

        nicknames.append(nickname)
        public_keys.append(public_key)
        clients.append(client)

        print(f'Nickname of {str(address)} is: {nickname}!')
        print(f'Public key of {str(address)} is: {public_key}')
        #client.send('Server: You are connected to the server!'.encode('utf-8'))
        #broadcast(f'Server: {nickname} has joined the chat!'.encode('utf-8'))

        if(len(nicknames) == 2):
            clients[1].send(f'Public key:{public_keys[0]}'.encode('utf-8'))
            clients[0].send(f'Public key:{public_keys[1]}'.encode('utf-8'))
            print("Public keys exchanged")
        

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is now listening...")
receive()
