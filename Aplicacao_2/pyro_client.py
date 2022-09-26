import Pyro4
import threading

@Pyro4.expose
@Pyro4.callback
class cliente_callback(object):
    
    def notificacao(self):
        print("callback recebido do servidor!")
            
    def loopThread(daemon):
        # thread para ficar escutando chamadas de método do servidor
        daemon.requestLoop()
     
    def main():
        # obtém a referência da aplicação do servidor no serviço de nomes
        ns = Pyro4.locateNS()
        uri = ns.lookup("NomeAplicacaoServidor")
        servidor = Pyro4.Proxy(uri)
        # ... servidor.metodo() —> invoca método no servidor
        # Inicializa o Pyro daemon e registra o objeto Pyro callback nele.
        daemon = Pyro4.core.Daemon()
        callback = cliente_callback() # callback será enviado ao servidor
        daemon.register(callback)
        # inicializa a thread para receber notificações do servidor
        # thread = threading.Thread(target=loopThread, args=(daemon, ))
        # thread.daemon = True
        # thread.start()