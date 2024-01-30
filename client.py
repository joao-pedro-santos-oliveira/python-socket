#importação de bibliotecas
from socket import *
import threading
import re

#inicialização de variáveis
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

    #checando se o usuário digitou o comando para se conectar
    if(mensagem.startswith(CONECTAR_SALA)):
        #enviando mensagem para o servidor para conectar o client
        sock.sendto(mensagem.encode(), serverAddress)
        user_name = extract_name(mensagem)
        print("Conectado com sucesso!")

        #inicializando as threads para enviar e receber mensagens
        thread_envio = threading.Thread(target=enviar_mensagens, args=[user_name])
        thread_recebimento = threading.Thread(target=receber_mensagens, args=())
        thread_envio.start()
        thread_recebimento.start()

    else:
        #caso o usuário tente enviar uma mensagem sem estar conectado
        print("Usuário não conectado!")
        main()

def receber_mensagens():
    #função para receber a mensagem do servidor e exibir na tela
    while True:
        clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
        clientMessageDecoded = clientMessage.decode()
        print(clientMessageDecoded)

def enviar_mensagens(user_name):
    #função para adicionar a mensagem num arquivo txt e enviar para o servidor
    while True:
        mensagem = input()
        #checando se o usuario deseja sair da sala
        if mensagem == SAIR_SALA:
            #caso queira, passamos a informação para o servidor e o usuário é desconectado, não podendo enviar mais mensagens
            full_message = f'<{user_name}>{mensagem}'
            sock.sendto(full_message.encode(), serverAddress)
            print("Usuário desconectado!")
            #return False para encerrar a função de enviar mensagem, já que o usuário se desconectou
            return False
        else:
            #criando/abrindo o arquivo txt em modo escrita e inserindo a mensagem
            with open("mensagens.txt", "w") as arquivo:
                full_message = f'<{user_name}>:{mensagem}'
                arquivo.write(full_message)

            #abrindo o arquivo em modo leitura
            with open("mensagens.txt", "r") as arquivo_leitura:
                #a variavel recebe os dados do buffer
                dados = arquivo_leitura.read(BUFFER_SIZE)
                #enquanto houverem dados a serem enviados, ele continuara enviando
                while dados:
                    sock.sendto(dados.encode(), serverAddress)
                    #caso não seja possivel enviar todos os bits de uma vez, variavel dados recebe o que faltou
                    dados = arquivo_leitura.read(BUFFER_SIZE)

if __name__ == "__main__":
    main()
