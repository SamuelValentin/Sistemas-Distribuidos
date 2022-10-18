# from asyncio.windows_events import NULL
import Pyro5.api
import threading

from compromisso import *

@Pyro5.api.expose
@Pyro5.api.callback

# Server ----------------

class cliente_callback(object):        
    def notificacao(self, msg):
        print("callback recebido do servidor! \n\n" + msg)
              
    def loopThread(self, daemon):
        # thread para ficar escutando chamadas de método do servidor
        daemon.requestLoop()
        
    def consulta_comp(self, nome_c, data, horario):
        print("_____________________")
        print(nome_c + " - " + data + " - " + horario) 
        
    def convidado_alerta(self, nome_c):
        print("Requisição do servidor: Digite 5")
        aux = input("Deseja receber notificação do compromisso " + nome_c + "?\n1-sim\n2-não\n")
        return aux
    
        
def criar_comp(servidor, referenciaCliente, nome):
        nome_c = input("Qual o nome do compromisso? ")
        data = input("Qual a data? ")
        horario = input("Qual o horario? ")
        num_conv = input("Quantos convidados? ")
        convidados_ = []
        if(int(num_conv) > 0):
            for i in range(int(num_conv)):
                convidado = input("Qual o nome do convidado? ")
                convidados_.append(convidado)
        
        servidor.cadastro_comp(referenciaCliente, nome, nome_c, data, horario, convidados_)

    
def main():
    # Obtém a referência da aplicação do servidor no serviço de nomes
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("AgendaServer")
    servidor = Pyro5.api.Proxy(uri)
    
    # Inicializa o Pyro daemon e registra o objeto Pyro callback nele.
    daemon = Pyro5.server.Daemon()
    callback = cliente_callback()
    referenciaCliente = daemon.register(callback)
    
    # Inicializa a thread para receber notificações do servidor
    thread = threading.Thread(target=callback.loopThread, args=(daemon, ))
    thread.daemon = True
    thread.start()
    print("Thread start")
    
    #init user ____________________________________________________
    nome = input("Escolha um nome de usuario: ")
    
    dict_ = {}
    
    # Invoca método no servidor, passando a referência
    servidor.cadastro_user(referenciaCliente, nome, dict_)
    # print(callback.get_pubKey())

    aux = 0
    while(aux != "0"): 
        aux = input("Escolha uma opcao:\n1 - Cadastrar compromisso\n2 - Consultar compromissos\n3 - Cancelar compromisso\n4 - Cancelar alerta\n0 - Sair\n\n")
        if(aux == "1"):
            criar_comp(servidor, referenciaCliente, nome)
        elif(aux == "2"):
            data = input("Qual seria a data?: ")
            print("Dia " + data + ". Compromissos: ")
            servidor.consulta_comp(referenciaCliente, nome, data)
        elif(aux == "3"):
            nome_c = input("Qual seria o compromisso?: ")
            servidor.cancelamento_comp(referenciaCliente, nome, nome_c)
        elif(aux == "4"):
            nome_c = input("Qual seria o compromisso?: ")
            servidor.cancelamento_alerta(referenciaCliente, nome, nome_c)
            
    

if __name__ == '__main__': 
    main()
