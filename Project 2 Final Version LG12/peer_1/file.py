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
   file_comparer(filepath,filepath2,filepath)
        

if __name__ == "__main__":
    main() 