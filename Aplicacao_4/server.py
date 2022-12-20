# Servidor ----------------------
class Servidor(object):    
    def init__():
        listaUser = open("listaUsers.txt","w+")
        print("Usuarios cadastrados:")
        print(listaUser.read())

    def cadastro_user(self, nome, referencia):   
        ver = verefica_User(nome)
        
        if ver == False:
            # Salvar Referencia do cliente
            listaUsers = open("listaUsers.txt","w+")
            listaUsers.writelines(str(nome) + ":" + str(referencia))

            # Cria arquivo com informacoes do Usuario
            listaC = open(str(nome) + "C.txt", "w+")
            listaC.writelines("Lista de Cartas")
            listaC.close()
            
            # Cria arquivo com amigos do Usuario
            listaA = open(str(nome) + "A.txt", "w+")
            listaA.writelines("Lista de amigos")
            listaA.close()
            
            return "cadastrado"
        else:
            return "Conectado"
        
    def verefica_User(nome):
        listaUsers = open("listaUsers.txt","w+")
        for users in listaUsers:
            if users == nome:
                return True
        return False
        
    def sorteia_Carta(nome):
        num = random.randint(1,52)
        carta = lista_cartas(num)
        adicionaCarta(nome, carta)

    def adicionaCarta(nome, carta):
        listaC = open(str(nome) + ".txt", "w+")
        listaC.writelines("MAN:" + carta)
        listaC.close()

    def removeCarta(nome, carta):
        listaC = open(str(nome) + "C.txt", "w+")  

        n = 0
        for l in listaC:
            if(l == carta):
                break
            n = n + 1

        for number, line in enumerate(listaC):
            if number not in [n]:
                listaC.write(line)

    def vereficaCarta(nome, carta):
        nomeF = open(str(nome) + "C.txt", "r")
        for itens in nomeF:
            if itens == carta:
                return True
        return False
    
    def mudaEstado(nome, carta, estado):
        cartas = open(str(nome) + "C.txt", "r")
        for itens in cartas:
            if itens(3,len) == carta:
                if itens(0,3) != "NEG":
                    carta.write(estado + carta)
                
    def enviaNot(ref, menssagem):
        user = cliente(ref)
        re = user.notificacaoR(menssagem)
        return re
        
    def abreTransação(comprador, refC, vendedor, cartaC, cartaV):
        # gera TID
        tid = geradorTid()
        print("TID: " + tid)

        # Verefica a existencia da carta
        ver = vereficaCarta(comprador, cartaC)
        if ver == False:
            return "Carta do comprador nao encontrada"

        ver = vereficaCarta(vendedor, cartaV)
        if ver == False:
            return "Carta do vendedor nao encontrada"
        
        # Busca a referencia do vendedor
        listaUsers = open("listaUser.txt","w+")
        for itens in listaUsers:
            if itens(0, vendedor.len) == cartaV:
                refV = itens(vendedor.len, len)
                
        mudaEstado(comprador, cartaC, "VEN")
        
        # Analisa o estado das cartas
        listaCartasV = open(vendedor + "c.txt","w+")
        for itens in listaCartasV:
            if itens(3, len) == cartaV:
                cartaV = itens
                
        listaCartasC = open(comprador + "c.txt","w+")
        for itens in listaCartasC:
            if itens(3, len) == cartaC:
                cartaC = itens

        #verifica o estado das cartas
        if(cartaC(0,3) == ven and cartaV(0,3) == ven):
            
            # Envia notifica para os participantes
            message = "Deseja realizar a tranasacao:"+ tid +" de troca da cartas '" + cartaC + "' e da '" + cartaV + "'?"
            vv = enviaNot(refV, message)     
            vc = enviaNot(refC, message)  
                    
            if vv == nao or vc == nao:
                mudaEstado(comprador, cartaC, "MAN")
                return "transacao cancelada"
            
            #Muda estado das cartas
            mudaEstado(comprador, cartaC, "NEG")
            mudaEstado(vendedor, cartaV, "NEG")

            # Troca de cartas inicializada
            # Backup feito
            backup = open("backup.txt", "r")
            CartaBackupV = "ven"+cartaV+"=1"
            CartaBackupC = "man"+cartaC+"=1"
            BackupV = "man"+cartaV+"=2"
            BackupC = "man"+cartaC+"=2"
            
            backup.write(CartaBackupV+"\n"+CartaBackupC+"\n"+BackupV+"\n"+BackupC)
            backup.close()

            # remove as cartas do comprador
            removeCarta(comprador, cartaC)
            vc = vereficaCarta(comprador, cartaC)
            
            if(vc == True):
                remove("backup.txt")
                return "Troca cancelada"
            
            # remove as cartas do vendedor
            removeCarta(vendedor, cartaV)
            vv = vereficaCarta(vendedor, cartaV)
            
            if(vv == True):
                #volta para o estado antigo
                restauraCarta(comprador, CartaBackupC,1)

                remove("backup.txt")
                return "Troca cancelada"

            # Add as cartas para o comprador
            adicionaCarta(comprador, cartaV)
            vc = vereficaCarta(comprador, cartaV)
            
            if(vc == False):
                restauraCarta(comprador, CartaBackupC,1)
                restauraCarta(vendedor, CartaBackupV,1)
                
                remove("backup.txt")
                return "Troca cancelada"
            
            # Add as cartas para o Vendedor
            adicionaCarta(vendedor, cartaC)
            vv = vereficaCarta(vendedor, cartaC)

            if(vv == False):
                restauraCarta(comprador, cartaV,2)
                restauraCarta(comprador, CartaBackupC,1)
                restauraCarta(vendedor, CartaBackupV,1)
                remove("backup.txt")
                return "Troca cancelada"

            remove("backup.txt")
            return "Troca realizada com sucesso"
        
        # Cartas em uma negociacao ja
        elif(cartaC(0,3) == neg or cartaV(0,3) == neg):
            print("Cartas ja estao em negociação")
            return "Cartas ja estao em negociação"

        # Cartas nao disponiveis pra troca
        elif(cartaV(0,3) == man):
            print("Cartas não estao em disponivels pra troca")
            return "Cartas não estao em disponivels pra troca"

    def consultaCartas(nome): 
        listaCartas = open(str(nome) + "C.txt", "r")
        lista = {}
        for itens in listaCartas:
            lista.add(itens)
            
        return lista
    
    def consultaAmigos(nome): 
        listaAmigos = open(str(nome) + "A.txt", "r")
        lista = {}
        for itens in listaAmigos:
            lista.add(itens)
            
        return lista
            
    def restaura():
        backup = open("backup.txt", "r")
        # Caso esteja vazio
        if backup == None:
            return "Nada a restaurar"
        else:
            for line in backup:
                itens = line
                cont = 0
                contT = 0
                for char in itens:
                    if char == "-":
                        break
                cont = cont + 1
                
                for char in itens:
                    if char == "=":
                        break
                contT = contT + 1
                
                restauraCarta(itens(cont,len),itens(0,cont), itens(contT,len))
                
    def restauraCarta(nome, carta, estado):
        if estado == 1:
            ver = vereficaCarta(nome, carta)
            if ver == True:
                return "ok"
            else:   
                adicionaCarta(nome, carta)
        else:
            ver = vereficaCarta(nome, carta)
            if ver == False:
                return "ok"
            else:   
                removeCarta(nome, carta)

def main():
    # Abre a aplicação para os clientes acessarem
    server = Servidor()
    servidor = register(server, "0.0.0.0")
    
    # Restaura caso tenha algo pendente
    servidor.restaura()
    
    print("A aplicação está ativa")
    servidor.requestLoop()
    

if __name__ == '__main__':
    main()