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
ACK = "ack"
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
        pattern = r'<.*>:(.*):<.*>'
        match = re.search(pattern, input_string)
    elif type == "checksum":
            pattern = r'<.*>:(.*):<(.*)>'
            match = re.search(pattern, input_string)

    if (match and type != "checksum"):
        return match.group(1)
    
    elif(match and type == "checksum"):
        return match.group(2)
    
    else:
        return None
    
def checksum(data):
    # Função para calcular o checksum
    checksum_value = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
            checksum_value += word
    while (checksum_value >> 16) > 0:
        checksum_value = (checksum_value & 0xFFFF) + (checksum_value >> 16)
    checksum_value = ~checksum_value & 0xFFFF
    return checksum_value

def is_package_ok(extracted_message_checksum, client_message_checksum):
    return extracted_message_checksum == client_message_checksum

def connect_client(clientAddress, user_name):
    #função para conectar os clients e adicionar o seu endereço na lista de clients conectados
    conected_clients.add(clientAddress)
    for client in conected_clients:
        #avisando a todos os clients que um novo client foi conectado
        connection_message = f'CONNECT {user_name} entrou na sala!'
        connection_message_checksum = checksum(connection_message.encode())
        connection_message_checksum_to_bytes = str(connection_message_checksum.to_bytes(4, byteorder="big"))
        connection_message = connection_message + connection_message_checksum_to_bytes

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

def extract_name_checksum_connect(input_string):
    partes = input_string.split()
    for i, parte in enumerate(partes):
        if parte.startswith("b'") and parte.endswith("'"):
            # Verifica se a parte anterior é o nome
            nome = partes[i - 1].strip("<>")
            checksum = parte.strip("b'")
            return nome, "b'" + checksum + "'"

def broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress):
    #função para retransmitir a mensagem recebida de um client para todos os clients conectados
    file_path = f'python-socket/message{user_port}.txt'
    #abrindo o arquivo em modo escrita e inserindo os dados
    with open(file_path, "w") as arquivo:
        full_message = f'<{user_ip}>:<{user_port}>/~{clientMessageDecoded} <{timestamp}>'
        arquivo.write(full_message)
    #abrindo o arquivo em modo leitura
    with open(file_path, "r") as arquivo_leitura:
        #a variavel recebe os dados do buffer
        dados = arquivo_leitura.read(BUFFER_SIZE)
        #enquanto houverem dados a serem enviados, ele continuara enviando
        if(clientAddress in conected_clients):
            for client in conected_clients:
                #enviando as mensagens fragmentadas para o usuario
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
        timestamp = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        #extraindo o nome do usuário e a mensagem em duas variáveis diferentes
        user_name = extract(clientMessageDecoded, "name")
        message = extract(clientMessageDecoded, "message")
        #checando se o client deseja se conectar
        if(clientMessageDecoded.startswith(CONECTAR_SALA)):
            checksum_user_message = f"{CONECTAR_SALA} <{user_name}>"
            client_message_checksum = checksum(checksum_user_message.encode())
            client_message_checksum_to_bytes = str(client_message_checksum.to_bytes(4, byteorder="big"))
            _, extracted_message_checksum = extract_name_checksum_connect(clientMessageDecoded)

            if(is_package_ok(extracted_message_checksum, client_message_checksum_to_bytes)):  
                connect_client(clientAddress, user_name)

        #checando se o client deseja se desconectar
        elif(message.startswith(SAIR_SALA)):
            remove_client(clientAddress, user_name)
        else:
            extracted_message_checksum = extract(clientMessageDecoded, "checksum")
            checksum_user_message = f"<{user_name}>:{message}:"
            client_message_checksum = checksum(checksum_user_message.encode())
            client_message_checksum_to_bytes = str(client_message_checksum.to_bytes(4, byteorder="big"))
            if(is_package_ok(extracted_message_checksum, client_message_checksum_to_bytes)):
            #retransmitindo para todos os clients
                broadcast(user_ip, user_port, clientMessageDecoded, timestamp, clientAddress)
                



if __name__ == "__main__":
    main()


                    


        

        