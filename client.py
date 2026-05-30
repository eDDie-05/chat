import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = input("Server IP: ")
PORT = 5555

client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)

        except:
            print("Connection closed.")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()