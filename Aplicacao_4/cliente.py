# Cliente ----------------------
class Cliente(object):
    def init__(Nome, referencia):
        self.nome = Nome
        self.referencia = Referencia

    def loopThread(self):
        # thread para ficar escutando chamadas de método do servidor
        openthread()

    def lista_cartas(servidor):
        lista = servidor.consultaCartas(self.nome)
        print(lista)

    def lista_amigos(servidor):
        lista = servidor.consultaAmigos(self.nome)
        print(lista)

    def adicionarAmigo(NomeA, servidor):
        aux = servidor.adicionarAmigo(NomeA, referencia, self.nome)
        if(aux == sim):
            lista_A.add(NomeA)
            print("Amigo adicionado")
        elif(aux == nao):
            print("pedido recusado")
        else:
            print("ERROR")

    def notificacaoR(menssagem):
        print(menssagem)
        re = input()
        return re

    def troca(servidor):
        vendedor = input("Qual seria o vendedor?")
        cartaC = input("Qual seria a sua Carta?")
        cartaV = input("Qual seria a Carta desejada?")
        
        menssagem = servidor.abreTransação(self.nome, self.referencia, vendedor, cartaC, cartaV)
        print(menssagem)
        
    def cartaVenda(servidor):
        carta = input("Qual seria a sua Carta?")
        servidor.mudaEstado(self.nome, carta, "VEN")
        
    def novaCarta(servidor):
        servidor.sorteia_Carta(self.nome)

def main():
    # Entrada do Usuario
    nome = input("")
    ref = geraRef()
    cliente = Cliente(nome, ref)
    cliente.loopThread()

    # conecta com servidor
    servidor = conectaServer(ReferenciaServidor)
    mensagem = servidor.cadastra_user(cliente.nome, cliente.referencia)
    print(mensagem)


    # Navegação
    input = 99
    while(input != 0):  
        print("Lista de opcoes")
        input_ = input()

        # Listar Cartas
        if(input_ == 1):
            cliente.listar_cartas(servidor)
        
        # Listar Amigos
        elif(input_ == 2):
            cliente.listar_amigos(servidor)
            
        # Adicionar Amigos
        elif(input_ == 3):
            cliente.adicionarAmigo(servidor)
            
        # Realizar Troca
        elif(input_ == 4):
            cliente.troca(servidor)

        # Nova Carta
        elif(input_ == 5):
            cliente.novaCarta(servidor)
            
        # Coloca Carta a venda
        elif(input_ == 6):
            cliente.cartaVenda(servidor)
            

