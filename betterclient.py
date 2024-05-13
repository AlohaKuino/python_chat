from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
from socket import SOL_SOCKET, SO_BROADCAST

class BetterClient(DatagramProtocol):
    def __init__(self, host, port): 
        if host == "localhost" : 
            host = "127.0.0.1"
        self.id = host, port
        self.address = None
        self.broadcast = '127.255.255.255', 8080
        self.server = '127.0.0.1', 9999
        self.initiator = False
        print("Working on id:", self.id)
    
    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if addr == self.server:
            print("Choose message type:\n1)Broadcast\n2)Direct")
            option = int(input())
            if( option == 1 ):
                self.broadcast_mode(parse_clients_string(datagram), datagram, addr)
            else:
                self.direct_mode(datagram, addr)
        else:
            if(datagram.__contains__("quit") and not(self.initiator)):
                print("user quit...so you can quit too")
            elif(datagram.__contains__("quit")):
                print("", end="")
                self.initiator = False
            elif(datagram.__contains__("broadcast")):
                print("\nfrom", addr[1], ":", datagram)
            else:
                print("\nfrom", addr[1], ":", datagram, "\nto" + str(self.address[1]) + " : ", end="")

    def direct_mode(self, datagram, addr):
        print("Write port to connect: ")
        port = input()
        if port.__contains__("quit"):
            print("Exiting")
            self.initiator = True
            self.datagramReceived(datagram, addr)
            return
        self.address = "127.0.0.1", int(port)
        reactor.callInThread(self.send_direct_message, datagram, addr)
    
    def send_direct_message(self, datagram, addr):
        while True:
            message = input("to " + str(self.address[1]) + " : ")
            if(message.__contains__("quit")):
                self.initiator = True
                self.transport.write(("quit").encode('utf-8'), self.address)
                self.datagramReceived(datagram.encode('utf-8'), addr)
                break
            self.transport.write(message.encode('utf-8'), self.address)
    
    def broadcast_mode(self, clients, datagram, addr):
        while True:
            message = input("broadcast: ")
            if message.__contains__("quit"):
                self.datagramReceived(datagram.encode('utf-8'), addr)
                break
            # for client in clients:
            #     address =  '127.0.0.1', client
            reactor.callInThread(self.send_broadcast_message, message)

    def send_broadcast_message(self, message):
        self.transport.write((message + "   this message is broadcast").encode('utf-8'), ('255.255.255.255', 8080))

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        self.transport.setBroadcastAllowed(True)
        self.transport.write("ready".encode('utf-8'), self.server)

def parse_clients_string(clients_string):
    if not clients_string:
        return []
    client_strings = clients_string.split('\n')
    clients = []
    for client_string in client_strings:
        client = parse_client_string(client_string)
        clients.append(client)
    return clients

def parse_client_string(client_string):
    client_string = client_string.strip('()')
    parts = client_string.split(',')
    port = int(parts[1].strip())
    return port

if __name__ == '__main__':
    port = randint(1000, 5000)
    reactor.listenUDP(port, BetterClient('127.0.0.1', port))
    reactor.run()
