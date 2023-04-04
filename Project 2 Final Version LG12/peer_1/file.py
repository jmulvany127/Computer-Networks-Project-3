import socket
import threading
import os.path
import time

from function_file import *

filepath = "DATABASE.txt"
filepath2 = "DATABASE2.txt"
filepath3 = "newDATABASE.txt"
token = "token.txt"
#merges filepath and filepath2 into filepath3
def main():
    file_comparer(filepath,filepath2,filepath3)
    print(count_lines(token))
    print (get_peer_location(token,1))
    print (get_peer_location(token,2))
    print (get_peer_location(token,3))
    

if __name__ == "__main__":
    main() 