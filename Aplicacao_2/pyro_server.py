from time import sleep
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
        
        # random_seed = Random.new().read
        # key_pair = RSA.generate(1024, random_seed)
        # pub_key = key_pair.publickey()
        
        # print(pub_key)
        
        cliente.set_pubKey()
        

    def cadastro_comp(self, referenciaCliente, nome, nome_c, data, horario, convidados_):
        print("Cadastro do compromisso: " + nome_c)
        
        comp = Compromisso(nome_c, data, horario, convidados_)
        
        dict_ = dictNomes[nome]
        dict_.update({nome_c : comp})
        
        th= threading.Thread(target=self.cadastro_alerta, args=(referenciaCliente, comp, nome))
        th.start()
        
        
    def cancelamento_comp(self, referenciaCliente, nome, comp):
        print("Cancelamento do compromisso")
        
        dict_ = dictNomes[nome]
        del dict_[comp]
        
    def cadastro_alerta(self, referenciaCliente, comp, nome):
        print("Cadastro do Alerta")
        
        convidados_ = []
        convidados = comp.get("convidados")
        
        for conv in convidados:
            try:
                conv_ref = dictRef[conv]
                cliente_conv = Pyro5.api.Proxy(conv_ref)
                aux = cliente_conv.convidado_alerta(comp.get("nome"))
                if aux == "1":
                    convidados_.append(conv)
            except KeyError:
                print("Usuario não encontrado")
        
        while(True):
            sleep(10)
            ini_time_for_now = datetime.now()
            notfica = ini_time_for_now + \
                            timedelta(minutes = 5)
            timer = notfica.strftime("%H:%M")
            if(str(timer) == comp.get("horario")):
                break
            
        try:
            dict_ = dictNomes[nome]
            ver = dict_[comp.get("nome")]
            print("Enviando not ")
            print(ver.get("nome"))
            
            cliente = Pyro5.api.Proxy(referenciaCliente)
            cliente.notificacao("Evento " + comp.get("nome") + " chegando em 5 minutos")
            
            for convidado in convidados_:
                referenciaConvidado_ = dictRef[convidado]
                
                cliente = Pyro5.api.Proxy(referenciaConvidado_)
                cliente.notificacao("Evento " + comp.get("nome") + " chegando em 5 minutos")
                
        except KeyError:
            print("Notificaçao cancelada...")
            
        
    def cancelamento_alerta(self, referenciaCliente, nome, comp):
        print("Cancelamento do compromisso")
        
    def consulta_comp(self, referenciaCliente, nome, data):
        cliente = Pyro5.api.Proxy(referenciaCliente)
        dict_ = dictNomes[nome]
        
        for comp in dict_.values():
            if data == comp.get("data"):
                cliente.consulta_comp(comp.get("nome"), comp.get("data"), comp.get("horario"))

def main():
    # registra a aplicação do servidor no serviço de nomes
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(servidor)
    ns.register("AgendaServer", uri)
    
    print("A aplicação está ativa")
    daemon.requestLoop()
    

if __name__ == '__main__':
    main()