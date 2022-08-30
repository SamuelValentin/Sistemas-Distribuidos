from email import message
import socket
import struct
import sys

import threading
import time
# from typing_extensions import Self

# Multicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Recive: Mensagem de Ola / Mensagem para anunciar o fim da eleicao
 
def multicastReciver(ip, port):
    print("Multicast - reciver start")
    print(ip, port)
    
    MCAST_GRP = '224.1.1.2'
    MCAST_PORT = input("digite a porta: ")
    
    print("on")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', int(MCAST_PORT)))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print(sock.recv(10240))
        
    # print(on + " \n")
    
    # multicast_addr = '228.0.0.1'
    # bind_addr = '0.0.0.0'
    # port = 3000

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # sock.bind((bind_addr, port))

    # for i in range(3):
    #     message, address = sock.recvfrom(255)
    #     print (message)
    
def multicastSend():
    print("Multicast - Send start")
    
    group = '224.1.1.2'
    port = 5678
    # 2-hop restriction in network
    ttl = 2
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_MULTICAST_TTL,
                    ttl)
    
    for i in range(1):   
        #input
        sock.sendto(b"as", (group, port))
        message = input("Menssagem: ")
    
    # # message = sys.argv[1] if len(sys.argv) > 1 else 'message via multicast'
    # # message = "Mengo"

    # multicast_addr = '228.0.0.1'
    # port = 3000

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ttl = struct.pack('b', 1)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    # sock.sendto(message.encode(), (multicast_addr, port))
    # sock.close()
        

# Uniicast ---------------------------------------------
# -> Init: thread (send / recive)
# -> Send/Recive: Mensagem de pedido de eleicao / Mensagem de resposta ao pedido de eleicao
       
def unicastReciver():
    print("Uniicast - reciver start")
    
def unicastSend():
    print("Uniicast - Send start")
    
# ------------------ Main -------------------------
def main():
    print("Bem vindo")  
    # ip = input("digite o ip: ")
    # port = input("digite a porta: ")  
    
    ip = '228.1.1.1'
    port = 6789
        
    # Inicia o multicast -- 
    trecive = threading.Thread(target=multicastReciver,args=(ip,port))
    trecive.start()
    tsend = threading.Thread(target=multicastSend)
    tsend.start()
        
    # Inicia o Unicast --    
    unicastReciver()
    unicastSend()
        
    state = 0
    # while(state != "1"):
    #     state = input("Digite 1 para sair ou 0 pra enviar: ")
    #     if(state == 0):
    #         p1.send(" ")
        

# -------------------------------------------------
if __name__ == '__main__':
    main()