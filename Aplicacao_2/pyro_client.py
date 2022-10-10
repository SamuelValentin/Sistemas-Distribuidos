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
        
    def criar_comp():
        comp = Compromisso(1,1,1,1)
        
        
    
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
    aux = input("Escolha um usuario:\n1-Sam\n2-Re\n3-John")
    
    if(aux == "1"):
        nome = "Sam"
        list_ = dictSam
    elif(aux == "2"):
        nome = "Re"
        list_ = dictRe
    elif(aux == "3"):
        nome = "John"
        list_ = dictJohn
    
    # Invoca método no servidor, passando a referência
    servidor.cadastro_user(referenciaCliente, nome, "Flamengo", "mengo")
    servidor.consulta_comp(referenciaCliente, nome, "_")
    

if __name__ == '__main__': 
    main()
