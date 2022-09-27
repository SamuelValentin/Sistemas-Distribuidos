# @Pyro4.expose
# # configura uma instância única do servidor para ser consumida por diversos
# @Pyro4.behavior(instance_mode="single")


# class servidor(object):
#     def main():
#     # registra a aplicação do servidor no serviço de nomes
#     daemon = Pyro4.Daemon()
#     ns = Pyro4.locateNS()
#     uri = daemon.register(servidor)
#     ns.register("NomeAplicacaoServidor”, uri)
#     daemon.requestLoop()
#     print("A aplicação está ativa")


# saved as greeting-server.py
import Pyro5.api

@Pyro5.api.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Tomorrow's lucky number is 12345678.".format(name)

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server
uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls