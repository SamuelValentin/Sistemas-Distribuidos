# Samuel Leal Valentin - 2023989 - Sistemas Distribuidos

from email import message
from itertools import count
import socket
# from socketserver import ThreadingUnixDatagramServer
import struct
import sys

import threading
import time
# from typing_extensions import Self

TIMERCOOR = 10
TIMERCOORV = 20
TIMERELEICAO = 15


eleicao = False
end = False
per = False
permissao = True
coordenadorVivo = True
coordenador_eleito = 7
id = 0

# Multicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Receive: Mensagem de Ola do coordenador/ Mensagem para anunciar o fim da eleicao
 
def multicastReceiver(ip1,port1):
    print("Multicast - receiver start")
    global coordenadorVivo, coordenador_eleito, eleicao, per, permissao
    
    group = '224.1.1.1'
    port = 8090
    
    MCAST_GRP = group
    MCAST_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    

    while True:
        data = str(sock.recv(10240))
        message = str(data)
        tam = len(message)
        if (message[2] == '1'): #Ola coordenador
            print(message[2 : tam])
            coordenadorVivo = True
            print("Ola")
        elif (message[2] == '2'): #Anuncio do Coordenador
            print(message[4 : tam])
            coordenador_eleito = message[4]
            print("Bem-vindo Chef")
            eleicao = False
            per = False
            permissao = True
        elif (message[2] == '4'): #Encerrar
            break

    
def multicastSend(state, id): 
    group = '224.1.1.1'
    port = 8090

    ttl = 2
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_MULTICAST_TTL,
                    ttl)
    
    if(state == 1): #  Ola a todos
        message = b"1-hello world" 
    elif(state == 2): # Mensagem de coordenador
        if(id == 1):
            message = b"2-1-Eu sou o Novo coordenador"
        elif(id == 2):
            message = b"2-2-Eu sou o Novo coordenador"
        elif(id == 3):
            message = b"2-3-Eu sou o Novo coordenador"
        elif(id == 4):
            message = b"2-4-Eu sou o Novo coordenador"

    elif(state == 4): # Finalizado
        message = b"4-Encerrando" 
    
    print(" Enviando ")
    sock.sendto(message, (group, port))

        
# Uniicast ---------------------------------------------
# -> Init: thread (send / receive)
# -> Send/Recive: Mensagem de pedido de eleicao / Mensagem de resposta ao pedido de eleicao

def unicastReceiver(ip ,port):
    print("Uniicast - reciver start")
    global permissao, coordenador_eleito, eleicao, coordenadorVivo
    eleicao = False

    UDP_IP = ip
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)

        message = str(data)
        # Pedido de eleicao
        if(message[2] == '1'): 
            #Pegando o ip e port do menssageiro 
            lista = listId()
            idB = int(message[4])
            ipB = lista[idB][1]
            portB = lista[idB][2]

            if(eleicao): #Eleicao ja iniciada
                unicastSend(ipB, portB, 2)         
            else: #Eleicao init
                while True:
                    if(eleicao):
                        unicastSend(ipB, portB, 2) 
                        break
                    elif(per):
                        break

                print("Mensagem de eleicao recebida: ")
                tam = len(data)
                print(data[2 : tam])
               

        # Negado o pedido de eleição        
        elif(message[2] == '2'):
            print("nao deu")
            permissao = False
            tv = threading.Thread(target=vericaCoordenador,args=(ip,port))
            tv.start()
            trecive = threading.Thread(target=multicastReceiver,args=(ip,port))
            trecive.start()

        elif(message[2] == '3'):
            print("Init HelloCoordenador")
            coordenador_eleito = id
            coordenadorVivo = True
            th = threading.Thread(target=multicastReceiver,args=(ip,port))
            th.start()
            tt = threading.Thread(target=helloCoordenador)
            tt.start()
            multicastSend(2, id)
            

        elif(message[2] == '4'):
            break
    
    
def unicastSend(ip, port, type):
    UDP_IP = ip
    UDP_PORT = port

    state = type
    if(state == 1): # Eleicao
        if(id == 1):
            message = b"1-1-quero ser o chefe"
        elif(id == 2):
            message = b"1-2-quero ser o chefe"
        elif(id == 3):
            message = b"1-3-quero ser o chefe"
        elif(id == 4):
            message = b"1-4-quero ser o chefe"
    elif(state == 2): # Resposta eleicao
        message = b"2-nao" 
    elif(state == 3): # Finalizacao do Timer
        message = b"3-TimerFinalizado" 
    elif(state == 4): # Finalizacao
        message = b"4-Encerrando" 

    MESSAGE = message

    print("\nMenssagem Enviada:  ")
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
# Lista de id init -------------------------------------

def listId():
    
    id0 = [0,'127.0.0.0', 1234]
    id1 = [1,'127.0.0.1', 6789]
    id2 = [2,'127.0.0.2', 5678]
    id3 = [3,'127.0.0.3', 4567]
    id4 = [4,'127.0.0.4', 3456]
    
    lista = [id0, id1, id2, id3, id4]
    
    return lista

# Mensagens --------------------------------------------

def timerElection(ip, port):
    global permissao
    time.sleep(TIMERELEICAO)
    if(permissao):
        unicastSend(ip, port, 3)
    
        
def envioEleicao():
    global id
    lista = listId()
    tam = len(lista)
    for i in range(id + 1 , tam):
        print(lista[i][1],lista[i][2])
        unicastSend(lista[i][1],lista[i][2],1)  
        
    timerElection(lista[id][1],lista[id][2])
        
def helloCoordenador():
    global end
    while True:
        if(end):
            break
        multicastSend(1, id)
        time.sleep(TIMERCOOR)
        

def vericaCoordenador(ip,port):
    global coordenadorVivo, end, eleicao, per
    while True:
        if(end):
            break
    
        time.sleep(TIMERCOORV)
        if(coordenadorVivo):
            coordenadorVivo = False
        elif(end != True):
            print("Erro no coordenador. Digite 1 para continuar\n")
            aux = input("Deseja começar uma eleicao?\n1-sim\n2-nao\n")
            if(aux == "1"):
                eleicao = True
                envioEleicao()
            else:
                unicastSend(ip,port,2)
                eleicao = False
                per = True

            time.sleep(TIMERCOORV)
            break
                
    
# ------------------ Main -------------------------
def main():
    global id, end

    # Inicializacao do ip e porta
    print("Bem vindo!\n") 
    lista = listId()
    length = len(lista)
    
    for i in range(length):
        print(lista[i])
    
    id = int(input("Escolha um id para começar: "))
    ip = lista[id][1]
    port = lista[id][2]
    
       
    # Inicia o multicast ------------------------------------ 
    trecive = threading.Thread(target=multicastReceiver,args=(ip,port))
    trecive.start()
        
    # Inicia o Unicast --------------------------------
    tUreceive = threading.Thread(target=unicastReceiver,args=(ip,port))
    tUreceive.start()
    
    if(id == coordenador_eleito):
        tt = threading.Thread(target=helloCoordenador)
        tt.start()
    else:
        tv = threading.Thread(target=vericaCoordenador,args=(ip,port))
        tv.start()
        
    state = 1    
    while True:
        state = input(" ")
        if(state == "0"):
            multicastSend(4, id)
            unicastSend(ip,port,4)
            end = True
            break
        

# -------------------------------------------------
if __name__ == '__main__':
    main()
