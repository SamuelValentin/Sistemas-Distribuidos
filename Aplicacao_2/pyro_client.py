import Pyro5.api
import threading
@Pyro5.api.expose
@Pyro5.api.callback

# Server ----------------

class cliente_callback(object):
    def notificacao(self, msg):
        print("callback recebido do servidor!")
              
    def loopThread(daemon):
        # thread para ficar escutando chamadas de método do servidor
        daemon.requestLoop()
        
    def criar_comp():
        comp = compromisso(1,1,1,1)
        
        
class compromisso():
     def __init__(self, nome, data, horario, convidados):
        self.nome = nome
        self.data = data
        self.horario = horario
        self.convidados = convidados
    
def main():
    # Obtém a referência da aplicação do servidor no serviço de nomes
    ns = Pyro5.api.locateNS()
    uri = ns.lookup("NomeAplicacaoServidor")
    servidor = Pyro5.api.Proxy(uri)
    # Inicializa o Pyro daemon e registra o objeto Pyro callback nele.
    daemon = Pyro5.server.Daemon()
    callback = cliente_callback()
    referenciaCliente = daemon.register(callback)
    # Invoca método no servidor, passando a referência
    servidor.cadastro(referenciaCliente, ...)
    # Inicializa a thread para receber notificações do servidor
    thread = threading.Thread(target=cliente_callback.loopThread, args=(daemon, ))
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    main()


# --------------------------------------------------------------------
# saved as greeting-client.py
# import Pyro5.api

# name = input("What is your name? ").strip()

# greeting_maker = Pyro5.api.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
# print(greeting_maker.get_fortune(name))