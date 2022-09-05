# chat server using multicast
# python fork of the original ruby implementation
# http://tx.pignata.com/2012/11/multicast-in-ruby-building-a-peer-to-peer-chat-system.html
# send.py
# usage : $ python send.py message

# import socket
# group = '224.1.1.1'
# port = 8090
# # 2-hop restriction in network
# ttl = 2
# sock = socket.socket(socket.AF_INET,
#                      socket.SOCK_DGRAM,
#                      socket.IPPROTO_UDP)
# sock.setsockopt(socket.IPPROTO_IP,
#                 socket.IP_MULTICAST_TTL,
#                 ttl)
# sock.sendto(b"hello world", (group, port))


# ---------------------------------------------------  Unicast

import socket
 
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))