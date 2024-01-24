# python-socket
Projeto de criação de socket para disciplina de redes de computadores.

Neste projeto, cada equipe desenvolverá um servidor de chat de sala única, onde os
clientes se conectam à sala e recebem todas as mensagens dos outros usuários, além de
também poderem enviar mensagens. Entretanto, essas mensagens não são strings como o
convencional, mas, a fim de haver transferência de arquivos e segmentação dos mesmos,
serão arquivos .txt que sendo lidos pelo servidor deverão ser impressos no terminal como
mensagens.
O projeto será composto por duas etapas, em que na primeira etapa o grupo deve
desenvolver uma ferramenta de troca de arquivos .txt e reverberar isso em um chat de
mensagens que utilize comunicação com UDP. Na segunda etapa, deverá ser
implementado ao chat básico de troca de mensagens já feito, um protocolo de transferência
confiável, utilizando UDP e o método RDT 3.0 apresentado em sala de aula.
A seguir, serão descritas as especificações e requisitos de cada uma das etapas:
1. Primeira Etapa: Transmissão de arquivos com UDP
● (4 pontos) Implementação de comunicação UDP utilizando a biblioteca Socket na
linguagem Python, com troca de arquivos em formato de texto (.txt) em pacotes de até
1024 bytes (buffer_size) em um chat de sala única, ou seja, apesar da troca inicial
entre os usuários ser em arquivos .txt, elas devem ser exibidas em linha de comando
no terminal de cada um dos clientes conectados à sala. (Não é necessária a
implementação de transferência confiável nessa etapa, somente na etapa 2).
● Prazo máximo de entrega: 01/02/2024
● Obs. 1: É necessário que o chat funcione para mais de um cliente simultaneamente, ou
seja, deverão ser abertos o terminal do servidor e ao menos dois terminais de clientes
sem que ocorra interrupção do funcionamento.
● Obs. 2: Arquivos .txt são normalmente maiores que mensagens podendo ultrapassar o
buffer_size (lembrando, de 1024 bytes), por isso nesse caso devem ser fragmentados
em pacotes e reconstruídos no receptor. É necessário que a aplicação seja capaz de
realizar essa fragmentação plenamente e que isso seja demonstrado.
● A implementação deverá ser realizada conforme os requisitos a seguir:
!!O que está em vermelho não é negociável!!
1. Cada mensagem deve aparecer no chat público, para cada usuário, no seguinte
formato:

<IP>:<PORTA>/~<nome_usuario>: <mensagem> <hora-data>
onde:
- <IP>: Endereço IP do emissor da mensagem
- <PORTA>: Número da porta do emissor da mensagem, do IP descrito acima.
- <nome_usuario>: nome do usuário
- <mensagem>: mensagem recebida
- <hora-data>: hora e data da mensagem recebida, de acordo com o horário
do servidor
Um exemplo de mensagem recebida é dado a seguir:
192.168.0.123:67890/~renato: Nosso estoque de comida está acabando. 14:31:26
03/02/2023

2. As funcionalidades serão executadas/solicitadas através de linhas de comando pelo
cliente e serão interpretadas pela aplicação. A tabela abaixo apresenta as
funcionalidades requeridas.
Funcionalidade Comando
Conectar à sala hi, meu nome eh
<nome_do_usuario>

Sair da sala bye
3. Quando um usuário se conectar à sala, os outros usuários deverão receber uma
mensagem de alerta da nova presença (ex: João entrou na sala).
4. Após estar conectado, qualquer mensagem enviada ao servidor será exibida na
íntegra para os outros usuários.

2. Segunda Etapa: Implementando chat com transferência confiável RDT 3.0
● (6 pontos) Implementação de um sistema de chat básico com transferência
confiável, segundo o canal de transmissão confiável rdt3.0, apresentado na
disciplina e presente no Kurose, utilizando-se do código resultado da etapa
anterior. A cada passo executado do algoritmo, em tempo de execução, deve
ser printado na linha de comando do servidor as etapas do processo, de modo a
se ter compreensão do que está acontecendo e demonstrar a coerência do
rdt3.0 implementado.
● Prazo máximo de entrega: 05/03/2024

● A implementação deverá ser realizada conforme os requisitos a seguir:
O RDT 3.0 pode parecer uma implementação complexa, mas torna-se mais
fácil quando há noção dos comportamentos que um algoritmo deve ter para ser
considerado um RDT 3.0. Abaixo estão os requisitos de avaliação e de
funcionamento, cada um deles tem um peso, proporcional a sua relevância e
complexidade, na nota desta etapa.
1. A capacidade mais básica a ser listada é a troca de mensagens entre os
participantes do chat. A recepção e encaminhamento de pacotes é fruto do
sucesso da primeira etapa do projeto e não traz nenhum aspecto de
confiabilidade implementado por intermédio do RDT 3.0;
2. É possível que haja corrupção de bits na troca de mensagens. Por isso, é
preciso que esses erros sejam detectados. Para isso, serve o “checksum”,
uma combinação de bits que acompanham o pacote e através de uma
complexidade matemática detectam se houve algum “erro de bit”. (Não se
preocupem a biblioteca os auxiliará significativamente);
3. O destinatário é capaz de perceber a integridade de um pacote através do
checksum e, caso não haja erros, retornar um pacote de confirmação ao
remetente conhecido como “ACK”;
4. O remetente aguarda a confirmação após enviar o pacote através do ACK,
caso não receba um ACK dentro do tempo de timeout, a mensagem deve
ser reenviada quantas vezes for necessário até que a confirmação seja
recebida pelo remetente;
5. Diante de um ACK que acabe sendo corrompido, haverá retransmissão de
pacotes. Para isso, é necessário haver o ‘número de sequência’ (podendo
ser de 1 bit ou mais), dessa forma o destinatário sabe se é uma
retransmissão ou não. Se eu envio como pacote 1,2,3,4,3, notoriamente o 3
em algum momento se corrompeu;
6. O número de sequência do pacote que está sendo reconhecido deve estar no
ACK;
7. Quando um pacote corrompido for recebido, basta reenviar o ACK do último
pacote recebido com sucesso. Portanto, ao detectar um ACK duplicado,
isso indica um problema no envio do pacote mais recente.
8. Adição e administração de timeouts que limitam o tempo, a qual confirma
uma perda quando não há o retorno de um ACK no tempo determinado,
assim utilizado para, em situações de perda de pacotes, detectá-las e
realizar retransmissão.

Instruções adicionais:
As atividades de cada etapa do projeto serão postadas no Google Classroom. A
equipe deve realizar todas as entregas para que a nota final (soma das notas das 2 etapas)
seja validada. Em cada etapa, deverá ser entregue, pelo Google Classroom, um link do
GitHub com uma pasta para cada entrega. A atividade deverá ser entregue por cada um
dos membros da equipe, nesses termos. Adicionalmente, para a última entrega, a equipe
deverá apresentar um vídeo com no máximo 15 minutos de duração. Nele, a equipe irá
explicar a implementação do código e seus componentes, além de mostrar o chat
funcionando. Todos os integrantes do grupo devem participar.
Cada entrega deve conter, em sua pasta, um README exclusivo daquela entrega,
com instruções de execução e eventuais observações necessárias. Comentem o código!
Cada equipe deve ser composta por, no máximo, 5 alunos. Será disponibilizada uma
tabela para a definição dos grupos com data de entrega até 05/12/2023. A nota final do
projeto vai compor 30% da média final da disciplina.
Obs: Em ambas as etapas, é fundamental que o código esteja limpo e legível. A
qualidade do código (sintaxe, organização, otimização...) será um critério importante na
avaliação do projeto, portanto, caprichem nesse aspecto!
