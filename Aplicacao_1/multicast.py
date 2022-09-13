from email import message
from itertools import count
import socket
import struct
import sys

import threading
import time
# from typing_extensions import Self
# Desktop/UTFPR/sd/Sistemas-Distribuidos/Aplicacao_1

# Mensagem:
# type-id-Message

# Multicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Receive: Mensagem de Ola / Mensagem para anunciar o fim da eleicao
 
def multicastReceiver():
    print("Multicast - receiver start")

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
        if (message[2] == '1'):
            print(message[2 : tam])
            print("Ola")
        elif (message[2] == '2'):
            print(message[2 : tam])
            print("Oi chef")
        elif (message[2] == '4'):
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
    
    sock.sendto(message, (group, port))

        

# Uniicast ---------------------------------------------
# -> Init: thread (send / receive)
# -> Send/Recive: Mensagem de pedido de eleicao / Mensagem de resposta ao pedido de eleicao
       
permissao = True

def unicastReceiver(ip ,port, id):
    print("Uniicast - reciver start")
    global permissao

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
                listaId = listaId()
                unicastSend(ip, port, 2)
                i = id
                for i in listaId:
                    unicastSend(listaId[i][1],listaId[i][2],1)
                timer = threading.Thread(target=timerElection,args=(ip,port))
                timer.start()

        # Negado o pedido de eleição        
        elif(message[2] == '2'):
            print("nao deu")
            permissao = False

        elif(message[2] == '3'):
            multicastSend(2)

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
    time.sleep(15)
    if(permissao):
        unicastSend(ip, port, 3)
    
    
# ------------------ Main -------------------------
def main():
    
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
    # tsend = threading.Thread(target=multicastSend)
    # tsend.start()
        
    # Inicia o Unicast --------------------------------
    tUreceive = threading.Thread(target=unicastReceiver,args=(ip,port,(id-1),))
    tUreceive.start()
    # tUsend = threading.Thread(target=unicastSend,args=(ip,port))
    # tUsend.start()
    
        
    state = 0
    multicastSend(1)
    while(state != "1"):
        state = input("Digite 0 para sair ou 1 pra enviar: ")
        if(state == "0"):
            break
        

# -------------------------------------------------
if __name__ == '__main__':
    main()