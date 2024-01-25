from socket import *

host ="localhost"
port = 11311
BUFFER_SIZE =1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
addr = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(addr)

conected_clients = set()

while True:
    clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
    clientMessageDecoded = clientMessage.decode()
    if(clientMessageDecoded.startswith(CONECTAR_SALA)):
        conected_clients.add(clientAddress)
        print(conected_clients)

    elif(clientMessageDecoded.startswith(SAIR_SALA)):
        if(clientAddress in conected_clients):
            conected_clients.remove(clientAddress)
        else:
            None
    else:
        if(clientAddress in conected_clients):
            for client in conected_clients:
                sock.sendto(clientMessageDecoded.encode(), client)

        else:
            None
        

        