import Pyro5.api
import threading

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
    def cadastro_user(self, referenciaCliente, name, msg):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        cliente.notificacao("Cadastrado...")
        
        thisdict.update({name: msg})
        
        
    def cadastro_comp(self, referenciaCliente, comp):
        print("Cadastro do compromisso")
        
    def cancelamento_comp(self, referenciaCliente, comp):
        print("Cancelamento do compromisso")
        
    def consulta_comp(self, referenciaCliente, name):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        cliente.notificacao(thisdict[name])
  

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
    
    
# ---------- Test hash map

# hm = HashMap(TAM_MAP +1)
# hm.put("1", "sachin", "a")
# hm.put("2", "sehwag", "a")
# hm.put("3", "ganguly", "a")

# print(hm.get("1"))
# print(hm.get("2"))
# print(hm.get("3"))
    
