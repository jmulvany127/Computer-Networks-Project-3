from Network import Network
from helpers.terminal_helper import print_colored

peer1 = Network('localhost', None, "Hospital A") #type in IP address if not localhost
print("Name of hospital:")
print(peer1.HOSPITAL)
peer1.start(5050)

print("SERVER-1 - Hospital A")
print_colored(f'PORT {peer1.SERVER_PORT} is started active', "green")


while True:
    print("Enter name of patient admitted:")
    data = input()

    peer1.broadcast(data)
