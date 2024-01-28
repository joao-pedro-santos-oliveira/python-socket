from socket import *
import re

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

    user_ip = clientAddress[0]
    user_port = clientAddress[1]
    palavras = clientMessageDecoded.split()
    if(clientMessageDecoded.startswith(CONECTAR_SALA)):
        conected_clients.add(clientAddress)

    elif(clientMessageDecoded.startswith(SAIR_SALA)):
        if(clientAddress in conected_clients):
            conected_clients.remove(clientAddress)
    else:
        with open("python-socket/mensagens.txt", "w") as arquivo:
            full_message = f'<{user_ip}>:<{user_port}>/~{clientMessageDecoded}'
            arquivo.write(full_message)

        with open("python-socket/mensagens.txt", "r") as arquivo_read:
            dados = arquivo_read.read(BUFFER_SIZE)
            if(clientAddress in conected_clients):
                for client in conected_clients:
                    sock.sendto(dados.encode(), client)
                    


        

        