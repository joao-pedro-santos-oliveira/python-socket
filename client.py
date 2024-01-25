from socket import *
import threading

host = "localhost"
port = 11311
BUFFER_SIZE = 1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
isOnline = False
serverAddress = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)




def main():
    mensagem = input("Para se conectar, escreva da seguinte forma 'hi, meu nome eh<seu_nome>'")

    if(mensagem.startswith(CONECTAR_SALA)):
        sock.sendto(mensagem.encode(), serverAddress)

        sock.sendto("entrou na sala!".encode('utf-8'), serverAddress)
        print("Conectado com sucesso!")

        thread_envio = threading.Thread(target=enviar_mensagens, args=())
        thread_recebimento = threading.Thread(target=receber_mensagens, args=())
        
        thread_envio.start()
        thread_recebimento.start()



def receber_mensagens():
    while True:
        clientMessage, clientAddress = sock.recvfrom(BUFFER_SIZE)
        clientMessageDecoded = clientMessage.decode()
        print(clientAddress, clientMessageDecoded)

def enviar_mensagens():
    while True:
        mensagem = input('Digite: ')
        if mensagem == SAIR_SALA:
            break
        elif mensagem.startswith(CONECTAR_SALA):
            sock.sendto(mensagem.encode(), serverAddress)
        else:
            with open("mensagens.txt", "w") as arquivo:
                arquivo.write(mensagem)

            with open("mensagens.txt", "r") as arquivo_leitura:
                dados = arquivo_leitura.read(BUFFER_SIZE)
                while dados:
                    sock.sendto(dados.encode(), serverAddress)
                    dados = arquivo_leitura.read(BUFFER_SIZE)

if __name__ == "__main__":
    main()
