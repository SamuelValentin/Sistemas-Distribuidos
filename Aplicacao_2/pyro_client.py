import Pyro5.api
import threading

from compromisso import *

@Pyro5.api.expose
@Pyro5.api.callback

# Server ----------------

class cliente_callback(object):
    def notificacao(self, msg):
        print("callback recebido do servidor! \n" + msg)
              
    def loopThread(daemon):
        # thread para ficar escutando chamadas de método do servidor
        daemon.requestLoop()
        
    def consulta_comp(self, nome_c, data):
        print(nome_c + " - " + data)
        
def criar_comp(servidor, referenciaCliente, nome):
        # nome_c = input("Qual o nome do compromisso?")
        # data = input("Qual a data?")
        # horario = input("Qual o horario?")
        nome_c = "Samuel"
        data = "28/10/22"
        horario = "18:00"
        # num_conv = input("Quantos convidados?")
        convidados_ = {}
        # if(int(num_conv) > 0):
        #     for i in range(int(num_conv)):
        #         convidado = input("nome convidado")
        #         convidados_.append(convidado)
                
        # comp = Compromisso(nome,data,horario,convidados_)
        
        servidor.cadastro_comp(referenciaCliente, nome, nome_c, data, horario, convidados_)

    
def main():
    # Obtém a referência da aplicação do servidor no serviço de nomes
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("NomeAplicacaoServidor")
    servidor = Pyro5.api.Proxy(uri)
    
    # Inicializa o Pyro daemon e registra o objeto Pyro callback nele.
    daemon = Pyro5.server.Daemon()
    callback = cliente_callback()
    referenciaCliente = daemon.register(callback)
    
    # Inicializa a thread para receber notificações do servidor
    thread = threading.Thread(target=cliente_callback.loopThread, args=(daemon, ))
    thread.daemon = True
    thread.start()
    print("Thread start")
    
    #init user ------------------------------------------
    # print("Escolha um usuario:\n1-Sam\n2-Re\n3-John")
    nome = input("Escolha um nome de usuario: ")
    
    # dict_ = {nome_c: comp}
    dict_ = {}
    
    # Invoca método no servidor, passando a referência
    servidor.cadastro_user(referenciaCliente, nome, dict_)
    
    criar_comp(servidor, referenciaCliente, nome)
    while(True): 
        aux = input("Escolha uma opcao:\n1 - Cadastrar compromisso\n2 - Consultar compromissos\n3 - Cancelar compromisso\n4 - Sair")
        servidor.consulta_comp(referenciaCliente, nome, "28/10/22")
    

if __name__ == '__main__': 
    main()
