from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self): 
        self.clients = set()

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        if datagram == "ready":
            adresses = "\n".join([str(client) for client in self.clients])
            self.transport.write(adresses.encode('utf-8'), addr)
            self.clients.add(addr)
        else:
            for client_address in self.clients:
                if client_address != addr:
                    self.transport.write(datagram.encode('utf-8'), client_address)

if __name__ == '__main__':
    reactor.listenUDP(9999, Server())
    reactor.run()
