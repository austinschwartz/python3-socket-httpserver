#!/usr/bin/env python3

import socket

class Server:
    def __init__(self, port = 90):
        self.port = port
        self.host = '0.0.0.0'

        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        self.conn, self.addr = self.socket.accept()
        print("Connection from: " + str(self.addr))
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break
            print("cocks: " + data)

        self.conn.close()



if __name__ == '__main__':
    s = Server(90)

