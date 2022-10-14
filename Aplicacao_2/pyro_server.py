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
    def cadastro_user(self, referenciaCliente, name, dict_):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        cliente.notificacao("Cadastrado...")
        
        dictNomes.update({name: dict_})
        dictRef.update({name: referenciaCliente})
        
        print(dictNomes)
        print(dictRef)
        

    def cadastro_comp(self, referenciaCliente, nome, nome_c, data, horario, convidados_):
        print("Cadastro do compromisso")
        
        comp = Compromisso(nome_c, data, horario, convidados_)
        
        dict_ = dictNomes[nome]
        dict_.update({nome_c : comp})
        
        d = dict_[nome_c]
        
        print(d.get("nome"))
        print(d.get("data"))
        print(d.get("horario"))
        
        
    def cancelamento_comp(self, referenciaCliente, nome, comp):
        print("Cancelamento do compromisso")
        
        dict_ = dictNomes[nome]
        del dict_[comp]
        
        
    def cadastro_alerta(self, referenciaCliente, nome, comp):
        print("Cadastro do Alerta")
        
    def cancelamento_alerta(self, referenciaCliente, nome, comp):
        print("Cancelamento do compromisso")
        
    def consulta_comp(self, referenciaCliente, nome):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        
        dict_ = dictNomes[nome]
        
        for comp in dict_.values():
            # comp = dict_[name_c]
            print(comp)
            n = comp.get("nome")
            d = comp.get("data")
            print(n + " - " + d)
            cliente.consulta_comp(n, d)

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
    
