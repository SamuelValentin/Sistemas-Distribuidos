# chat server using multicast
# python fork of the original ruby implementation
# http://tx.pignata.com/2012/11/multicast-in-ruby-building-a-peer-to-peer-chat-system.html
# receiver.py
# usage : $ python receiver.py  # wait for messages to come in


# import socket
# import struct
# MCAST_GRP = '224.1.1.1'
# MCAST_PORT = 8090
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.bind(('', MCAST_PORT))
# mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
# while True:
#     print(sock.recv(10240))
    
# Uniscast ------------------------------------

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

i=0
while (i < 2):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    i += 1