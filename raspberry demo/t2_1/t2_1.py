import socket
import threading
import os.path
import time
###READ ME- DEAL WITH D_IP WITH SOME FORM OF QUEUE
###COMMMENT and tidy up code (p_port and p- adres)

from q import*
from function_file_t2 import *

BUFFER_SIZE = 65536
SEPARATOR = "<SEPARATOR>"

#arrays for storing adresses of peers
d_ip = 1
port = []


#file location and size
filepath = "T2DATABASE.txt"



peers_in_t1 =3
max_attempts = peers_in_t1*3
rfrsh_code = 9999


#ip and port numbers
l_ip = '10.35.70.42'   #local ip- insert device ip here 

udp_s_port = (33777)     #source port for sender

tcp_s_port = (33779)  #tcp local server address
tcp_s_adr = ( l_ip, tcp_s_port) #tcp local server address

file_rcvd = False

d_ip = Queue() #queue which holds new peers ips
p_port = Queue() #queue which holds new peer addresses 

            

#function opened in new thread
#function sets up a tcp server socket for receiving messages from peers
def file_server():
    file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_server.bind(tcp_s_adr)
    while True:
        global file_rcvd
        #print('entered tcp server thread\n')
        
        file_server.listen(10)
        
       # print(f"[*] Listening as file server {tcp_s_adr}")
        client_socket, address = file_server.accept()
       # print(f"[+] T1 is connected.") ###REMOVE THIS
        

        
        #while loop reads in bytes, saves bytes and then overwrites local file with these bytes 
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f = open(filepath, "wb")
            f.write(bytes_read)
        print (f"Database update received from Tier 1")
        file_rcvd = True 
        client_socket.close()
        
        




        
#function to send typed messages to peer
def send_my_adrs( t1_port):
            global udp_s_port          
            #opens the udp sending socket 
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_sock.bind((l_ip, udp_s_port))
            

            #print(udp_d_port) Debug
            
            #get the destination port from the queue
            d_ip1 = d_ip.dequeue()
            #print(d_ip1) Debug
            #make the destination adress
            d_adrs = (str(d_ip1),t1_port)
            #print(d_adrs)
            #print(d_adr)Debug
            my_adrs = (l_ip + "," + str(tcp_s_port))
            #print(my_adrs)
            #send our token to peer so they can verify we are trusted
            send_sock.sendto(str(rfrsh_code).encode(), d_adrs)
            time.sleep(0.01)
            send_sock.sendto(my_adrs.encode(), d_adrs)

            send_sock.close()
            
       
                    


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

def get_file():
    global file_rcvd
    attempts = 0
    while(file_rcvd == False ):
        attempts = attempts + 1
        if(attempts == max_attempts):
            print("No tier 1 devices online, database refresh unavailable.")
            file_rcvd = True
            break
        
        random_num = get_random_number(1, peers_in_t1)
        random_num = str(random_num)
        #print(random_num)
        peer_to_ip_and_port(random_num)
        t1_port = int(port[0])
        
        send_my_adrs(t1_port)
        #print ("adress sent")
        time.sleep(0.5)   

def main():
    global file_rcvd
    file_rcvr = threading.Thread(target=file_server, daemon=True)
    file_rcvr.start()
   
    time.sleep(0.2)
    while True:  
        print("Commands: 'view' view the current database,'rfrsh' retrieve latest database version")
        cmd = input('Enter command: \n')
        file_rcvd = False
        if(cmd == 'view'):
            print_Dbase()
       
        elif (cmd == 'rfrsh'):
            get_file()
            file_rcvd = False
            get_file()

            
            
     
if __name__ == "__main__":
    main() 