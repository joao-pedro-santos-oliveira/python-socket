from socket import *
import re
from datetime import *

host ="localhost"
port = 11311
BUFFER_SIZE =1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
addr = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(addr)

conected_clients = set()

def extract(input_string, type):
    # Expressão regular para extrair o nome do usuário
    if type == "name":
        pattern = r'<(.*?)>'
        match = re.search(pattern, input_string)
    elif type == "message":
        pattern = r'<.*?>(.*)'
        match = re.search(pattern, input_string)
    
    if match:
        # Retorna o primeiro grupo de captura que corresponde ao nome do usuário
        return match.group(1)
    else:
        return None

def connect_client(clientAddress, user_name):
    conected_clients.add(clientAddress)
    for client in conected_clients:
        connection_message = f'{user_name} entrou na sala!'
        sock.sendto(connection_message.encode(), client)

def remove_client(clientAddress, user_name):
    if(clientAddress in conected_clients):
        removed_message = f'{user_name} saiu do chat!'
        for client in conected_clients:
            if(client != clientAddress):
                sock.sendto(removed_message.encode(), client)
        conected_clients.remove(clientAddress)

def broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress):
    with open("python-socket/mensagens.txt", "w") as arquivo:
        full_message = f'<{user_ip}>:<{user_port}>/~{clientMessageDecoded} {timestamp}'
        arquivo.write(full_message)

    with open("python-socket/mensagens.txt", "r") as arquivo_read:
        dados = arquivo_read.read(BUFFER_SIZE)
        if(clientAddress in conected_clients):
            for client in conected_clients:
                sock.sendto(dados.encode(), client)

def main():
    while True:
        clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
        clientMessageDecoded = clientMessage.decode()
        user_ip = clientAddress[0]
        user_port = clientAddress[1]
        timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        user_name = extract(clientMessageDecoded, "name")
        message = extract(clientMessageDecoded, "message")

        if(clientMessageDecoded.startswith(CONECTAR_SALA)):
            connect_client(clientAddress, user_name)
            
        elif(message.startswith(SAIR_SALA)):
            remove_client(clientAddress, user_name)
        else:
            broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress)

if __name__ == "__main__":
    main()


                    


        

        