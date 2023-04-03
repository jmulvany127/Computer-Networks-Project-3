from Network import Network
from helpers.terminal_helper import print_colored


peer2 = Network('localhost', None, "Hospital B") #type in IP address if not localhost
peer2.start(5051)


print("SERVER-2 - Hospital B")
print_colored(f'PORT {peer2.SERVER_PORT} is started active', "green")

peer2.join_network()

while True:
    print("Enter name of patient admitted:")
    data =input()

    peer2.broadcast(data)





