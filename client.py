from socket import *

host = "localhost"
port = 11311
BUFFER_SIZE = 1024
SAIR_SALA = "bye"
CONECTAR_SALA = "hi, meu nome eh"
isOnline = False
serverAddress = (host, port)
sock = socket(AF_INET, SOCK_DGRAM)




# Abre o arquivo no modo leitura e escrita
with open("mensagens.txt", "r+") as arquivo:
    while True:
        mensagem = input('Digite: ')
        if(mensagem == SAIR_SALA):
            False
        elif(mensagem.startswith(CONECTAR_SALA)):
            sock.sendto(mensagem.encode(), serverAddress)

        else:
            arquivo.write(mensagem)
            
            # Volta para o início do arquivo para lê-lo
            arquivo.seek(0)
            
            dados = arquivo.read(BUFFER_SIZE)

            while dados:
                sock.sendto(dados.encode(), serverAddress)
                dados = arquivo.read(BUFFER_SIZE)
