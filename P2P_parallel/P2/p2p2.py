import socket
import threading
import os.path
import time
###READ ME- DEAL WITH D_IP WITH SOME FORM OF QUEUE
###COMMMENT and tidy up code (p_port and p- adres)

from q import*
from function_file import *

BUFFER_SIZE = 65536
SEPARATOR = "<SEPARATOR>"

#arrays for storing adresses of peers
d_ip = 1
port = []

#ranges for potential tokens 
upper = 99999999999999
lower = 100000
#file location and size
filepath = "C:\\Users\\jsmul\\Desktop\\College Year 3\\Semester 2\\3D3 Computer Networks\\Project 2\\project 2 repo\\Final v3\\6 p2p local demo\\DATABASE2.txt"
filesize = os.path.getsize(filepath)


my_p_num = '2'     #peer number of this device
current_p_num = 0  #peer number of peer in current connection 
my_token = 1       #gloabl variable declaration, will be replaced in functions

#number of connections
connections = 0

#ip and port numbers
l_ip = '10.35.70.21'   #local ip- insert device ip here 

udp_l_port = (33000 + int(my_p_num))     #listening port
udp_s_port = (33100 +  int(my_p_num)*10)     #source port for sender

tcp_s_port = (33150 + 10*int(my_p_num) )  #tcp local server address
tcp_s_adr = ( l_ip, tcp_s_port) #tcp local server address

rsp_d_ip = '127.0.0.1' #ip address of most recent peer, will be edited by functions 

d_ip = Queue() #queue which holds new peers ips
p_port = Queue() #queue which holds new peer addresses 
bfr = Queue() #buffer for listening server data 

alarm_state = True #for different messager functionality
             
#function opened in new thread
#function sets up a tcp server socket for receiving messages from peers
def msg_server():
    #print('entered tcp server thread\n') #debug
    
    msg_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_server.bind(tcp_s_adr)
    msg_server.listen(10)
    
    print(f"[*] Listening as message server {tcp_s_adr}")
    client_socket, address = msg_server.accept()
    print(f"[+] peer {current_p_num} is connected.")
    
    recieved = 'blank'
    while (recieved != ''):
        recieved = client_socket.recv(1024)
        recieved = recieved.decode('utf-8')
        print((recieved))

    msg_server.close()
    
    #decrements the connections when socket closed
    global connections 
    connections = connections - 1

#function opened in new thread
#function sets up a tcp server socket for receiving messages from peers
def file_server():
       #print('entered tcp server thread\n')
    file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_server.bind(tcp_s_adr)
    file_server.listen(10)
    
    print(f"[*] Listening as file server {tcp_s_adr}")
    client_socket, address = file_server.accept()
    print(f"[+] peer {current_p_num} is connected.")

    #while loop reads in bytes, saves bytes and then overwrites local file with these bytes 
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f = open(filepath, "wb")
        f.write(bytes_read)
    print ("Database received")
    #    progress.update(len(bytes_read))
    client_socket.close()
    file_server.close()
    
    #decrements the connections when socket closed
    global connections 
    connections = connections - 1

#function opened in new thread
#function sets up an always on udp server socket for receiving messages from peers  
def listen():
    #declare access to gloabl buffer queue
    global bfr
    
    #bind udp listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((l_ip, udp_l_port))
    #print ('listening',({l_ip},{udp_l_port}))
    
    
    while True:
        
        #blocking call reads in and decodes data 
        rcvd_data = sock.recv(1024).decode('utf-8')
        print (f"received data {rcvd_data}") #debug
        
        #add data to buffer queue
        bfr.enqueue(rcvd_data)
        
        #while data is in buffer hadnle it 
        while(bfr.size()>0):
            
            data = bfr.dequeue()
            print (f"buffered data {data}")
            
            #if data is in right range to be a token
            if ((int(data) >= lower and int(data) <= upper) ):
                
                #check if token is in trusted peers file and assign the address to result 
                result = ip_fetcher(data)
                #print(f'peer:{result[0]} {result[1]} connected\n')
                
                #if not reset msg command
                if (result == False):
                    print("Enter peer number:")
                    return
                else:
                    #print(f'peer:{result[0]} {result[1]} connected\n')
                    
                    #marker for file or text data
                    marker = sock.recv(1024).decode('utf-8')
                    #increments connection count
                    global connections 
                    connections = connections + 1
                    
                    #update tcp_s port and address, this is where our local tcp server socket will be binded to 
                    global tcp_s_port
                    tcp_s_port = tcp_s_port + connections
                    global tcp_s_adr
                    tcp_s_adr = (l_ip, tcp_s_port)
                    
                    #update the address of the peers udp listening server by parsing result
                    global rsp_d_ip
                    rsp_d_port = int(result[1])
                    rsp_d_ip = (result[0])
                    rspd_adrs = (rsp_d_ip, rsp_d_port )
                    
                    #get the peer number of the current peer
                    global current_p_num        
                    current_p_num = result[2]
                    
                    #open TCP Server thread for incoming files
                    if (marker == 'f'):
                        f_server = threading.Thread(target=file_server, daemon=True)
                        f_server.start()
                    #open tcp server thread for incoming messages
                    elif (marker == 't'):
                        m_server = threading.Thread(target=msg_server, daemon=True)
                        m_server.start()
                    
                    #send our local tcp server port to the peer
                    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_sock.bind((l_ip, udp_s_port))
                    send_sock.sendto((str(tcp_s_port)).encode(), (rspd_adrs))
                    send_sock.close()
                    #print(f"server address{tcp_s_adr}sent to udp port{udp_d_port}") #debug
                
            #numbers in this range are receved tcp port numbers
            elif (int(data) >= 30000 and int(data) <=60000):
                #update the peer port 
                global p_port
                p_port.enqueue(int(data))               
                print(f"new peer address received {int(data)}") #debug                                                                 
            else:
                print ("data unrecognised, connection blocked\n")
        

#function to send typed messages to peer
def send_message( udp_d_port):
            global udp_s_port          
            global alarm_state
            #opens the udp sending socket 
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_sock.bind((l_ip, udp_s_port))
            
            #increment the udp source port for parallel connections
            udp_s_port = (udp_s_port + 1)
            #print(udp_d_port) Debug
            
            #get the destination port from the queue
            d_ip1 = d_ip.dequeue()
            #print(d_ip1) Debug
            #make the destination adress
            d_adr = (str(d_ip1),udp_d_port)
            #print(d_adr)Debug
            
            #send our token to peer so they can verify we are trusted
            send_sock.sendto(str(my_token).encode(), d_adr)
            
            time.sleep(0.1)
            
            #send the marker t to the peer so they know they will be recieiving a message
            marker = 't'
            send_sock.sendto(marker.encode(), (str(d_ip1), udp_d_port))
            send_sock.close()
            
            #decrement udp source port number
            udp_s_port = (udp_s_port - 1)
           
            
            
            time.sleep(0.2)
            #waits for peer to send back the tcp port number, received will be true here
            print(f"waiting for the peer socket address")
            #will run aslong as there are destination ports in teh queue
            while (p_port.size() >0):
                                   
                #open tcp client and send message to peer tcp peer 
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                p_tcp_addr = (str(d_ip1),p_port.dequeue())
                print(p_tcp_addr)#debug
                
                msg = 'alarm'
                s.connect((p_tcp_addr))
                if (alarm_state == True):
                    msg = msg.encode('utf-8')
                    s.send(msg)
                    
                else:
                    while(msg != 'quit' ):
                        #accept user input for message
                        if (msg != 'quit' ):
                            msg = input('Input peer message, enter quit to exit messenger: \n ').encode('utf-8')
                            s.send(msg)
                            msg = msg.decode('utf-8')
                s.close() 
                    
                break 
        
#function to send files to peer        
def send_file( udp_d_port):
    
    global udp_s_port
    #opens the udp sending socket 
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.bind((l_ip, udp_s_port))
    
    #increment the udp source port for parallel connections
    udp_s_port = (udp_s_port + 1)
    #print(udp_d_port) Debug
    
    #get the destination port from the queue
    d_ip1 = d_ip.dequeue()
    #print(d_ip1) Debug
    #make the destination adress
    d_adr = (str(d_ip1),udp_d_port)
    #print(d_adr)Debug
    
    #send our token to peer so they can verify we are trusted
    send_sock.sendto(str(my_token).encode(), d_adr)
    
    time.sleep(0.1)
    
    #send the marker t to the peer so they know they will be recieiving a file
    marker = 'f'
    send_sock.sendto(marker.encode(), (str(d_ip1), udp_d_port))
    send_sock.close()
    
    #decrement udp source port number
    udp_s_port = (udp_s_port - 1)
    time.sleep(0.2)
    #waits for peer to send back the tcp port number, received will be true here
    print(f"waiting for the peer socket address")
 
    while (p_port.size() >0):
        while True:
            
            #open tcp client and sends file to peer tcp peer 
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            p_tcp_addr = (str(d_ip1),p_port.dequeue())
            print(p_tcp_addr)#debug
            
            s.connect((p_tcp_addr))
            #msg = 'blank'
            #while(msg != 'send' ):
                #msg = input('Input send for file transfer \n ')
                #wait for send comand to send file (for testing )
                #if (msg == 'send' ):
                    #reads file in byte wise and sends final packet to peer
            with open(filepath, "rb") as f:                               
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
                    print ("Database sent")

                s.close()
                            
            break

#function to print the current data base        
def print_Dbase():
    with open(filepath, "r") as file:
        
        file_contents = file.read()
        print(file_contents)

#function to handle user inputted peer number and return address if peer recognised    
def peer_to_ip_and_port(number):
    
    check = number_check(number)
    if (check ==False):
        return False
    correctnums =splitting(number)
    storage = []
    global d_ip
    global port
    storage = addres_arrays(correctnums)
    d_ip_array = ip_array(storage)
    d_ip.enqueue(d_ip_array[0])
    port = port_array(storage)
    return True 
    #shouldnt need to anything else as ip+port should be in the global array but declared in there respective functions idk at this point

def file_broadcast_update():
    total_peers = 3
    for x in range(total_peers):
        p = str(x +1)
        if(p != my_p_num):
            peer_to_ip_and_port(p)
            udp_d_port = int(port[0])
            filer = threading.Thread(target=send_file, daemon=True, args=[ udp_d_port])
            filer.start()

def alarm_broadcast():
    global alarm_state
    total_peers = 3
    for x in range(total_peers):
        alarm_state = True
        p = str(x +1)
        if(p != my_p_num):
            peer_to_ip_and_port(p)
            udp_d_port = int(port[0])
            filer = threading.Thread(target=send_message, daemon=True, args=[udp_d_port])
            filer.start()
    

def main():
    
    #starts the listener thread
    listener = threading.Thread(target=listen, daemon=True)
    listener.start()
    
    #gets token number of this device frm file and update gloabl variable
    global my_token
    my_token = get_my_token(my_p_num)
  
    
    while True:  
        #wait for previous actions to complete and print to console 
        time.sleep(0.5)
        print("Commands: \n 'cnct' -connect to peer to peer \n 'view' -view the current database \n 'add' -to add to the database")
        print(" 'alrm' -Send Emergency notification to all peers \n 'brdcst' -Manually broadcast a file update \n ")
        cmd = input('Enter command: \n')

        if(cmd == 'view'):
            print_Dbase()
        elif(cmd == "add"):
            if (database_insert(filepath) != True):
                file_broadcast_update()
        elif (cmd == 'brdcst'):
            file_broadcast_update()
        elif (cmd == 'alrm'):
            alarm_broadcast()
        elif (cmd == 'cnct'):
            global alarm_state
            alarm_state = False
            peer = input('Enter peer number:\n')
            check = peer_to_ip_and_port(peer)
            #print(check)
            if(check == False):
                continue
            else:
                udp_d_port = int(port[0])
            
                #print(f"{udp_d_port}\n")
            print("Commands: 'msg' -talk to peer, 'file', send database to peer")
            cmd = input('Enter command: \n')
            
            if (cmd == 'msg'):
                send_message( udp_d_port)
            elif(cmd == 'file'):
                send_file( udp_d_port)

            
        
if __name__ == "__main__":
    main() 