#!/usr/bin/python
#encoding:utf-8
import socket
import threading
SIZE = 4096
class Test:
    def __init__(self):
        sock_svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_svr.bind(('localhost', 1122))
        sock_svr.listen(1)
        self.server, addr = sock_svr.accept()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('192.166.53.1', 22))
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
    t = Test()
    t1 = threading.Thread(target=t.clients)
    t2 = threading.Thread(target=t.servers)
    t2.start()
    t1.start()
