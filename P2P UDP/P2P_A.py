import socket
#import sys
import threading

#ip and port numbers
l_ip = '10.73.65.187'   #local ip
ip = '10.35.70.21'     #dest ip
#ports 33000 - 33999
udp_l_port = 33000       #listening port
udp_s_port = 33001       #source port for sender
udp_d_port = 33002       #destination port for sender


# function opens a socket and is always listening, ready to receive messages
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((l_ip, udp_l_port))
    print ('listening')
    
    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')
        
#starts a new thread that runs the listening function
listener = threading.Thread(target=listen, daemon=True);
listener.start()

#opens the sending socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((l_ip, udp_s_port))

#reads in input and sends to peer
print ('talk to your friends!')
while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, udp_d_port))