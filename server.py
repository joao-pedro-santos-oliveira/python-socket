#importação de bibliotecas
from socket import *
import re
from datetime import *

#inicialização de variáveis
host ="localhost"
port = 11311
BUFFER_SIZE =1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
addr = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)

#fazendo um bind do endereço do servidor para que ele permaneça sempre o mesmo
sock.bind(addr)

#para armazenar a lista de clients conectados
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
        return match.group(1)
    else:
        return None

def connect_client(clientAddress, user_name):
    #função para conectar os clients e adicionar o seu endereço na lista de clients conectados
    conected_clients.add(clientAddress)
    for client in conected_clients:
        #avisando a todos os clients que um novo client foi conectado
        connection_message = f'{user_name} entrou na sala!'
        sock.sendto(connection_message.encode(), client)

def remove_client(clientAddress, user_name):
    #função para remover o client, fazendo com que ele não receba mais as mensagens enviadas
    if(clientAddress in conected_clients):
        removed_message = f'{user_name} saiu do chat!'
        for client in conected_clients:
            #avisando aos clients que um client foi desconectado
            if(client != clientAddress):
                sock.sendto(removed_message.encode(), client)
        conected_clients.remove(clientAddress)

def broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress):
    #função para retransmitir a mensagem recebida de um client para todos os clients conectados
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
        #recebendo o arquivo do client
        clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
        clientMessageDecoded = clientMessage.decode()
        #identificando o IP do client e a porta
        user_ip = clientAddress[0]
        user_port = clientAddress[1]
        #pegando a data/hora o horario da mensagem e formatando
        timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        #extraindo o nome do usuário e a mensagem em duas variáveis diferentes
        user_name = extract(clientMessageDecoded, "name")
        message = extract(clientMessageDecoded, "message")

        #checando se o client deseja se conectar
        if(clientMessageDecoded.startswith(CONECTAR_SALA)):
            connect_client(clientAddress, user_name)

        #checando se o client deseja se desconectar
        elif(message.startswith(SAIR_SALA)):
            remove_client(clientAddress, user_name)
        #enviando a mensagem extraida do arquivo txt para todos os clients
        else:
            broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress)

if __name__ == "__main__":
    main()


                    


        

        