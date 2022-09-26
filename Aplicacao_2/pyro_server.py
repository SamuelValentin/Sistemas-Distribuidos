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