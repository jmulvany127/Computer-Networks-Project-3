from Network import Network


from helpers.terminal_helper import print_colored


peer3 = Network('localhost', None, "Hospital C") #type in IP address if not localhost
peer3.start(5052)


print("SERVER-3 - Hospital C")
print_colored(f'PORT {peer3.SERVER_PORT} is started active Please enter a key to continue', "green")



peer3.join_network()

while True:
    print("Enter name of patient admitted:")
    data =input()

    peer3.broadcast(data)





