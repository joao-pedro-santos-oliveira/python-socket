from socket import *
import threading
import re

host = "localhost"
port = 11311
BUFFER_SIZE = 1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
serverAddress = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)

def extract_name(input_string):
    # Expressão regular para extrair o nome do usuário
    pattern = r'<(.*?)>'
    match = re.search(pattern, input_string)
    if match:
        # Retorna o primeiro grupo de captura que corresponde ao nome do usuário
        return match.group(1)
    else:
        return None

def main():
    mensagem = input("Para se conectar, escreva da seguinte forma 'hi, meu nome eh<seu_nome>'")

    if(mensagem.startswith(CONECTAR_SALA)):
        sock.sendto(mensagem.encode(), serverAddress)
        user_name = extract_name(mensagem)
        print("Conectado com sucesso!")

        thread_envio = threading.Thread(target=enviar_mensagens, args=[user_name])
        thread_recebimento = threading.Thread(target=receber_mensagens, args=())
        
        thread_envio.start()
        thread_recebimento.start()

    else:
        print("Usuário não conectado!")
        main()

def receber_mensagens():
    while True:
        clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
        clientMessageDecoded = clientMessage.decode()
        print(clientMessageDecoded)

def enviar_mensagens(user_name):
    while True:
        mensagem = input()
        if mensagem == SAIR_SALA:
            full_message = f'<{user_name}>{mensagem}'
            sock.sendto(full_message.encode(), serverAddress)
            print("Usuário desconectado!")
            return False
        else:
            with open("mensagens.txt", "w") as arquivo:
                full_message = f'<{user_name}>:{mensagem}'
                arquivo.write(full_message)

            with open("mensagens.txt", "r") as arquivo_leitura:
                dados = arquivo_leitura.read(BUFFER_SIZE)
                while dados:
                    sock.sendto(dados.encode(), serverAddress)
                    dados = arquivo_leitura.read(BUFFER_SIZE)

if __name__ == "__main__":
    main()
