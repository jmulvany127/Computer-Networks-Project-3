import socket
import threading
import os.path
import time

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
filepath = "DATABASE1.txt"
filesize = os.path.getsize(filepath)


my_p_num = '1'     #peer number of this device
current_p_num = 0  #peer number of peer in current connection 
my_token = 1       #gloabl variable declaration, will be replaced in functions

#number of connections
connections = 0

#ip and port numbers
l_ip = '127.0.0.1'   #local ip- insert device ip here 

udp_l_port = (50000 + int(my_p_num))     #listening port
udp_s_port = (50100 +  int(my_p_num))     #source port for sender

tcp_s_port = (50000 + 10*int(my_p_num) )  #tcp local server address
tcp_s_adr = ('127.0.0.1', tcp_s_port) #tcp local server address

rsp_d_ip = '127.0.0.1' #ip address of most recent peer, will be edited by functions 
p_port = 50000 #base port for new peers, will be edited by functions
p_addr = (rsp_d_ip, p_port) #global variable base address for new peers will be edited by functions




rcved = False #boolean to indicate whether or not peer TCP Connection recievd

lock = threading.Lock()

             
#function opened in new thread
#function sets up a tcp server socket for receiving messages from peers
def msg_server():
    print('entered tcp server thread\n') #debug
    
    msg_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_server.bind(tcp_s_adr)
    msg_server.listen(10)
    
    print(f"[*] Listening as message server {tcp_s_adr}")
    client_socket, address = msg_server.accept()
    print(f"[+] peer {current_p_num} is connected.")
    
    recieved = client_socket.recv(1024)
    recieved = recieved.decode('utf-8')
    print((recieved))
    print(f"from peer {current_p_num}")

    msg_server.close()
    
    #decrements the connections when socket closed
    global connections 
    connections = connections - 1

#function opened in new thread
#function sets up a tcp server socket for receiving messages from peers
def file_server():
    print('entered tcp server thread file1\n')
    file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_server.bind(tcp_s_adr)
    file_server.listen(10)
    
    print(f"[*] Listening as file server {tcp_s_adr}")
    client_socket, address = file_server.accept()
    print(f"[+] peer {current_p_num} is connected.")
    #received = client_socket.recv(BUFFER_SIZE).decode()
    #filename, filesize = received.split(SEPARATOR)
    
    #filename = os.path.basename(filename)
    #filesize = int(filesize)
    #progress bar
    #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #while loop reads in bytes, saves bytes and then overwrites local file with these bytes 

    if lock.locked():  # debug
        print(f"Mutex already locked, sorry peer {current_p_num}")  # debug
    else:
        print(f"Mutex free to lock, go ahead peer {current_p_num}")
    # acquire the lock
    lock.acquire()
    print(f"Mutex acquired by peer {current_p_num}")
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f = open(filepath, "wb")
        f.write(bytes_read)
    print (f"Database received from peer {current_p_num}")
    time.sleep(10)
    #mutex unlock
    lock.release()
    print(f"Mutex unlocked by peer {current_p_num}") #debug
    #    progress.update(len(bytes_read))
    client_socket.close()
    file_server.close()



    #decrements the connections when socket closed
    global connections 
    connections = connections - 1

#function opened in new thread
#function sets up an always on udp server socket for receiving messages from peers  
def listen():\
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((l_ip, udp_l_port))
    #print ('listening',({l_ip},{udp_l_port}))
    
    
    while True:
        #blocking call reads in and decodes data 
        data = sock.recv(1024).decode('utf-8')
        #print (f"received data {data}") #debug
        
        #if data is in right range to be a token
        if ((int(data) >= lower and int(data) <= upper) ):
            result = ip_fetcher(data)
            #print(f'peer:{result[0]} {result[1]} connected\n')
    
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
                
                #update the port number of the peers udp listening port 
                
                rsp_d_port = int(result[1])
                
                global rsp_d_ip
                rsp_d_ip = (result[0])
                rspd_adrs = (rsp_d_ip, rsp_d_port )
                
                global current_p_num        
                current_p_num = result[2]
                
                #open TCP Server thread
                if (marker == 'f'):
                    f_server = threading.Thread(target=file_server, daemon=True)
                    f_server.start()
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
        elif (int(data) >= 50000 and int(data) <=60000):
            #update the peer port 
            global p_port
            p_port = int(data)
            
            global p_addr
            p_addr = (str(d_ip), p_port)
            #print(f"new peer address received {p_addr}") #debug
            global rcved
            
            #upate the received variable
            rcved = True 
            
        else:
            print ("data unrecognised, connection blocked\n")

#function to send typed messages to peer
def send_message( udp_d_port):
            #opens the udp sending socket 
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_sock.bind((l_ip, udp_s_port))
            
            #print(udp_d_port)
            #print(d_ip)
            
            d_adr = (str(d_ip),udp_d_port)
            #print(d_adr)
            
            #include d_ips //////////////////////////////////////////////////////////////////
            send_sock.sendto(str(my_token).encode(), d_adr)
            
            time.sleep(0.1)
            marker = 't'
            send_sock.sendto(marker.encode(), (str(d_ip), udp_d_port))
            send_sock.close()
            
           
            global p_port 
            global rcved
            
            time.sleep(0.2)
            #waits for peer to send back the tcp port number, received will be true here
            print(f"waiting for the peer socket address")
            while True:
                if (rcved == True):
                    #open tcp client and send message to peer tcp peer 
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    #print(p_addr)
                    
                    s.connect((p_addr))
                    msg = input('Input peer message: \n ').encode('utf-8')
                    s.send(msg)
                    s.close()
                    rcved = False
                    p_port = 50000
                    break 
        
#function to send files to peer        
def send_file( udp_d_port):
    
     d_adr = (str(d_ip),udp_d_port)
     send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     send_sock.bind((l_ip, udp_s_port))
     send_sock.sendto(my_token.encode(), (d_adr))
     time.sleep(0.1)
     marker = 'f'
     send_sock.sendto(marker.encode(), (d_adr))
     send_sock.close()
     #opens the udp sending socket 
     
     global p_port 
     global rcved
     
     time.sleep(0.2)
     #waits for peer to send back the tcp port number, received will be true here
     #print(f"waiting for the peer socket address")
     while True:
        if (rcved == True):
            #open tcp client and sends filename and size to peer tcp peer 
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((p_addr))
            #s.send(f"{filepath}{SEPARATOR}{filesize}".encode())
            
            #prints local progress message
            #filename = os.path.basename(filepath)
           # progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            
            #reads file in byte wise and sends final packet to peer
            with open(filepath, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
                    print ("Database sent")
                  #  progress.update(len(bytes_read))
            s.close()
            
            rcved = False
            p_port = 50000
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
    d_ip = d_ip_array[0]
    port = port_array(storage)
    return True 
    #shouldnt need to anything else as ip+port should be in the global array but declared in there respective functions idk at this point



def main():

    
    #starts the listener thread
    listener = threading.Thread(target=listen, daemon=True)
    listener.start()
    
    #gets token number of this device frm file and update gloabl variable
    global my_token
    my_token = get_my_token(my_p_num)
  
    time.sleep(0.2)
    while True:  
        print("Commands: 'cnct' -connect to peers to peer, 'view' view the current database, 'add' to add to the database")
        cmd = input('Enter command: \n')

        if(cmd == 'view'):
            print_Dbase()
        elif(cmd == "add"):
            database_insert(filepath)
        elif (cmd == 'cnct'):
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