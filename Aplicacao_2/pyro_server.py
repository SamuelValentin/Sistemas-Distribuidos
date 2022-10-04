import Pyro5.api
import threading
@Pyro5.api.expose
# configura uma instância única do servidor para ser consumida por diversos clientes
# @Pyro4.behavior(instance_mode="single")


# -------- Métodos do Servidor ---------
# • Cadastro de usuário (valor 0,3):
# • Cadastro de compromisso (valor 0,7):
# • Cancelamento de compromisso ou alerta (valor 0,2):
# • Consulta de compromissos (valor 0,3):

# Hash map

class servidor(object):
    def cadastro_user(self, referenciaCliente, msg):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        cliente.notificacao(msg)
        
    def cadastro_comp(self, referenciaCliente, comp):
        print("Cadastro do compromisso")
        
    def cancelamento_comp(self, referenciaCliente, comp):
        print("Cancelamento do compromisso")
        
    def consulta_comp(self, referenciaCliente):
        print("Consulta do compromisso")
        
def main():
    # registra a aplicação do servidor no serviço de nomes
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(servidor)
    ns.register("NomeAplicacaoServidor", uri)
    
    print("A aplicação está ativa")
    daemon.requestLoop()
    

if __name__ == '__main__':
    main()
    
# -----------------------------------------------------------------------
# saved as greeting-server.py
# import Pyro5.api

# @Pyro5.api.expose
# class GreetingMaker(object):
#     def get_fortune(self, name):
#         return "Hello, {0}. Here is your fortune message:\n" \
#                "Tomorrow's lucky number is 12345678.".format(name)

# daemon = Pyro5.server.Daemon()         # make a Pyro daemon
# ns = Pyro5.api.locate_ns()             # find the name server
# uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
# ns.register("example.greeting", uri)   # register the object with a name in the name server

# print("Ready.")
# daemon.requestLoop()                   # start the event loop of the server to wait for calls