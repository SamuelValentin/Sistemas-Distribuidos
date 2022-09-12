from email import message
from itertools import count
import socket
from socketserver import ThreadingUnixDatagramServer
import struct
import sys

import threading
import time
# from typing_extensions import Self
# Desktop/UTFPR/sd/Sistemas-Distribuidos/Aplicacao_1

TIMERCOOR = 15
TIMERCOORV = 20
TIMERELEICAO = 15

coordenadorVivo = True
coordenador_eleito = 4
id = 0

# Multicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Receive: Mensagem de Ola do coordenador/ Mensagem para anunciar o fim da eleicao
 
def multicastReceiver():
    print("Multicast - receiver start")
    global coordenadorVivo
    
    group = '224.1.1.1'
    port = 8090
    
    MCAST_GRP = group
    MCAST_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    i=0
    
    while (i < 5):
        i += 1
        message = str(sock.recv(10240))
        tam = len(message)
        if (message[2] == '1'): #Ola coordenador
            print(message[2 : tam])
            coordenadorVivo = True
            print("Ola")
        elif (message[2] == '2'): #Anuncio do Coordenador
            print(message[2 : tam])
            print("Bem-vindo Chef")
        elif (message[2] == '4'): #Encerrar
            break
    
    
def multicastSend(state): 
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
        message = b"2-Eu sou o Novo coordenador"
    elif(state == 4): # Finalizado
        message = b"4-Encerrando" 
    
    sock.sendto(message, (group, port))

        

# Uniicast ---------------------------------------------
# -> Init: thread (send / receive)
# -> Send/Recive: Mensagem de pedido de eleicao / Mensagem de resposta ao pedido de eleicao
       
permissao = True

def unicastReceiver(ip ,port):
    print("Uniicast - reciver start")
    global permissao, coordenador_eleito

    UDP_IP = ip
    UDP_PORT = port

    print(ip)
    print(port)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    i=0
    while (i < 10):
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        i += 1

        message = str(data)
        # Pedido de eleicao
        if(message[2] == '1'):
            tam = len(data)
            print(data[2 : tam])
            aux = input("Deseja ser o coordenador:\n1-Sim\nNao\n")
            if(aux == 1):
                unicastSend(ip, port, 2)
                timer = threading.Thread(target=envioEleicao)
                timer.start()

        # Negado o pedido de eleição        
        elif(message[2] == '2'):
            print("nao deu")
            permissao = False

        elif(message[2] == '3'):
            coordenador_eleito = id
            multicastSend(2)
            tc = threading.Thread(target=helloCoordenador)
            tc.start()

        elif(message[2] == '4'):
            break
    
    
def unicastSend(ip, port, type):
    # print("Uniicast - Send start")

    UDP_IP = ip
    UDP_PORT = port

    state = 0
    if(state == 1): # Eleicao
        message = b"1-quero ser o chefe" 
    elif(state == 2): # Resposta eleicao
        message = b"2-nao" 
    elif(state == 3): # Finalizacao do Timer
        message = b"3-TimerFinalizado" 
    elif(state == 4): # Finalizacao
        message = b"4-Encerrando" 

    MESSAGE = message

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
    time.sleep(TIMERELEICAO)
    if(permissao):
        unicastSend(ip, port, 3)
    
        
def envioEleicao():
    listaId = listaId()
    i = id+1
    for i in listaId:
        unicastSend(listaId[i][1],listaId[i][2],1)       
    timerElection(listaId[i][id],listaId[i][id])
        
def helloCoordenador():
    while True:
        multicastSend(1)
        time.sleep(TIMERCOOR)

def vericaCoordenador():
    while True:
        time.sleep(TIMERCOORV)
        if(coordenadorVivo):
            coordenadorVivo = False
        else:
            aux = input("Deseja começar uma eleicao?\n1-sim\n2-nao")
            if(aux == 1):
                envioEleicao()
    
    
# ------------------ Main -------------------------
def main():
    global id
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
    trecive = threading.Thread(target=multicastReceiver)
    trecive.start()
        
    # Inicia o Unicast --------------------------------
    tUreceive = threading.Thread(target=unicastReceiver,args=(ip,port,(id-1),))
    tUreceive.start()
    
    if(id == coordenador_eleito):
        tc = threading.Thread(target=helloCoordenador)
        tc.start()
        
    state = 0
    multicastSend(1)
    while True:
        state = input("Digite 0 para sair")
        if(state == 0):
            multicastSend(4)
            unicastSend(4)
            break
        

# -------------------------------------------------
if __name__ == '__main__':
    main()