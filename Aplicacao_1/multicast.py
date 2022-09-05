from email import message
import socket
import struct
import sys

import threading
import time
# from typing_extensions import Self
# Desktop/UTFPR/sd/Sistemas-Distribuidos/Aplicacao_1

# Multicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Receive: Mensagem de Ola / Mensagem para anunciar o fim da eleicao
 
def multicastReceiver():
    print("Multicast - receiver start")

    group = '224.1.1.1'
    port = 8090
    
    MCAST_GRP = group
    MCAST_PORT = port
    
    print("on")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print(sock.recv(10240))
    
    
def multicastSend():
    print("Multicast - Send start")
    
    # 2-hop restriction in network
    group = '224.1.1.1'
    port = 8090
    # 2-hop restriction in network
    ttl = 2
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_MULTICAST_TTL,
                    ttl)
    sock.sendto(b"hello world", (group, port))

        

# Uniicast ---------------------------------------------
# -> Init: thread (send / receive)
# -> Send/Recive: Mensagem de pedido de eleicao / Mensagem de resposta ao pedido de eleicao
       
def unicastReceiver(ip ,port):
    print("Uniicast - reciver start")

    UDP_IP = ip
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    i=0
    while (i < 2):
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        i += 1
    
    
def unicastSend(ip, port):
    print("Uniicast - Send start")

    UDP_IP = ip
    UDP_PORT = port
    MESSAGE = b"Hello, World!"

    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
# Lista de id init -------------------------------------

def listId():
    
    id1 = [1,'127.0.0.1', 6789]
    id2 = [2,'127.0.0.2', 5678]
    id3 = [3,'127.0.0.3', 4567]
    id4 = [4,'127.0.0.4', 3456]
    
    lista = [id1, id2, id3, id4]
    
    return lista
    
    
# ------------------ Main -------------------------
def main():
    
    # Inicializacao do ip e porta
    print("Bem vindo!\n") 
    lista = listId()
    length = len(lista)
    
    for i in range(length):
        print(lista[i])
    
    id = int(input("Escolha um id para começar: "))
    ip = lista[id-1][1]
    port = lista[id-1][2]
    
       
    # Inicia o multicast -- 
    trecive = threading.Thread(target=multicastReceiver,args=(ip,port))
    trecive.start()
    tsend = threading.Thread(target=multicastSend)
    tsend.start()
        
    # Inicia o Unicast -- 
    # tUreceive = threading.Thread(target=unicastReceiver)
    # tUreceive.start()
    # tUsend = threading.Thread(target=unicastSend)
    # tUsend.start()
    
        
    state = 0
    # while(state != "1"):
    #     state = input("Digite 1 para sair ou 0 pra enviar: ")
    #     if(state == 0):
    #         p1.send(" ")
        

# -------------------------------------------------
if __name__ == '__main__':
    main()