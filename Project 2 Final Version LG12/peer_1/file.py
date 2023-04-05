import socket
import threading
import os.path
import time

from function_file import *

filepath = "DATABASE.txt"
filepath2 = "DATABASE2.txt"
filepath3 = "newDATABASE.txt"
token = "token.txt"
filepath4 = "PUBLICDATABASE.txt"
#merges filepath and filepath2 into filepath3
def main():
   read_and_print_fields(filepath,filepath4)
        

if __name__ == "__main__":
    main() 