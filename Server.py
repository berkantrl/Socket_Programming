from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 44444
BUFFERSIZE = 1024 
ADDR = (HOST,PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def message(): # Gelen mesajların kontrolünü sağlayan fonksiyon
    pass
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected." %client_address)
        client.send(bytes("Welcome to chat application \nPlease input your name", "utf8"))
        addresses[client] = client_address
        Thread(target=client_connect, args=(client,)).start()


def client_connect(client): # client bağlantısını bağlayan fonksiyon
    name = client.recv(BUFFERSIZE).decode("utf8")
    welcome = "Welcome {}.Type 'exit' to exit ".format(name)
    client.send(bytes(welcome, "utf8"))
    msg = "{} is connect to channel".format(name)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name 
    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("exit", "utf8"):
            broadcast(msg, name + ": ")
        else :
            client.send(bytes("exit","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("{} is exit to channel".format(name),"utf8"))
            break 

def broadcast(msg, name = ""):
    for yayin in clients:
        yayin.send(bytes(name, "utf8")+msg)
        
if __name__ == "__main__":
    try:
        SERVER.listen(10) # maksimum 10 kişi bağlanabilir.
        print("Bağlantı bekleniyor...")
        ACCEPT_THREAD = Thread(target=message)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except KeyboardInterrupt:
        exit()

