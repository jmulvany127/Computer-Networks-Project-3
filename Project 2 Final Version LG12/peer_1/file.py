import socket
import threading
import os.path
import time

from function_file import *

filepath = "test_DATABASE.txt"
filepath2 = "DATABASE2.txt"
filepath3 = "newDATABASE.txt"
token = "token.txt"
filepath4 = "test_PUBLICDATABASE.txt"
#merges filepath and filepath2 into filepath3
def main():
    print("Commands: 'cnct' -connect to peers to peer, 'view' view the current database, 'add' to add to the database")
    cmd = input('Enter command: \n')
    if(cmd == "add"):
            first =input ("do you wish to add to database (y/n):")
            if (first == "y"):
                     name =input("type in the persons name,If this is unkown, leave this section blank:")
                     apperance= input("type in the persons Apperance,If this is unkown, leave this section blank:")
                     seen_last =input("type in the persons last seen,If this is unkown, leave this section blank:")
                     status = input("type in the persons status,If this is unkown, leave this section blank:")
                     #db_insert(filepath4,name,apperance,seen_last,status)
                     database_insert(filepath,name,apperance,seen_last,status)
                     time.sleep(0.2)
                     db_insert(filepath4,name,apperance,seen_last,status)
        

if __name__ == "__main__":
    main() 