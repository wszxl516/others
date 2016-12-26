#!/usr/bin/python
#encoding:utf-8
import socket
import threading
import sys
SIZE = 4096

class Test:
    def __init__(self, host, hostport, mapport ):
        sock_svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_svr.bind(('localhost', mapport))
        sock_svr.listen(1)
        self.server, addr = sock_svr.accept()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, hostport))
    def clients(self):
        while True:
            data = self.client.recv(SIZE)
            print('recv:', len(data))
            self.server.send(data)
        self.client.close()
    def servers(self):
        while True:
            data = self.server.recv(SIZE)
            print('send:', len(data))
            self.client.send(data)
        self.erver.close()
if __name__ == '__main__':
    if len(sys.argv) >= 4:
        t = Test(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        t1 = threading.Thread(target=t.clients)
        t2 = threading.Thread(target=t.servers)
        t2.start()
        t1.start()
    else:
        print('Usage:\n\t{0} [remote addr] [remote port] [local port]'.format(sys.argv[0]))
        
