This folder contains all files neccessary to do an IPC demonstration of our project
i.e. demonstrate it locally on one device that is running multuple command windows, with each window running a different node

Each of the p2pX.py files contains the python code for a node, X = the peer number of that node
	For example if i am running  p2p2.py and p2p5.py and the p2p5.py user will enter the peer number 2 wehn prompted to establish comms with p2p2.py
Each of the DATABASEX.txt files contains the missing persons database currently stored on the corresponding node
	For example DATABASE3 will store the current database for p2p3.py
The Tokens file contaons the list of all trusted peers in teh network, each peer in the file contains the following data:
	Peer number- Again this is the number that another peer will enter when it wishes to communicate to this peer	
	Socket Adress- This is the IP adress and port number of each peers listening server, if one peer wishes to communicate
		       with another they must first be authenitcated through the listening server
	Token- This 12 digit number is used to authenticate each trusted peer
	Note taht each peer would typiclaly have it's own IP address however this is a local demo
Ther function file contains a number of functions to be used by the main p2pX.py node files

Note that there is only one token and function file here as they will be the same on each node and so can be shared for the local demo 
