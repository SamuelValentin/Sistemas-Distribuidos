import Pyro5.api
import threading

from hashmap import *
from compromisso import *

@Pyro5.api.expose
# configura uma instância única do servidor para ser consumida por diversos clientes
# @Pyro4.behavior(instance_mode="single")


# -------- Métodos do Servidor ---------
# • Cadastro de usuário (valor 0,3):
# • Cadastro de compromisso (valor 0,7):
# • Cancelamento de compromisso ou alerta (valor 0,2):
# • Consulta de compromissos (valor 0,3):

# Servidor Agenda ----------------------
class servidor(object):
    # def __init__(self):
        
    #     lista = HashMap(TAM_MAP + 1)
    #     lista.put("1", "sachin", "a")
    #     lista.put("2", "sehwag", "a")
    #     lista.put("3", "ganguly", "a")
        
    #     for i in range(3):
    #         print(self.lista.get(i))

    #     self.lista = lista
    
    def cadastro_user(self, referenciaCliente, msg):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        cliente.notificacao(msg)
        
    def cadastro_comp(self, referenciaCliente, comp):
        print("Cadastro do compromisso")
        
    def cancelamento_comp(self, referenciaCliente, comp):
        print("Cancelamento do compromisso")
        
    def consulta_comp(self, referenciaCliente):
        print("Consulta do compromisso")
        for i in range(3):
            print(self.lista.get(i))
  

def main():
    # registra a aplicação do servidor no serviço de nomes
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(servidor())
    ns.register("NomeAplicacaoServidor", uri)
    
    print("A aplicação está ativa")
    daemon.requestLoop()
    



if __name__ == '__main__':
    main()
    
    
# ---------- Test hash map

# hm = HashMap(TAM_MAP +1)
# hm.put("1", "sachin", "a")
# hm.put("2", "sehwag", "a")
# hm.put("3", "ganguly", "a")

# print(hm.get("1"))
# print(hm.get("2"))
# print(hm.get("3"))
    
