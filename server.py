#!/usr/bin/env python3
from threading import Thread
import socketserver, subprocess, sys
from pathlib import Path

class RequestHandler(socketserver.BaseRequestHandler):
    def sendOK(self):
        self.request.send('HTTP/1.0 200 OK\r\n'.encode('utf8'))

    def sendDenied(self):
        self.request.send('HTTP/1.0 403 Permission Denied\r\n'.encode('utf8'))
    
    def sendNF(self):
        self.request.send('HTTP/1.0 404 Not Found\r\n'.encode('utf8'))

    def sendContentType(self, file_path):
        extension = file_path.rsplit('.', 1)[1]
        if extension == 'html' or extension == 'htm':
            content_type = 'text/html'
        elif extension == 'png':
            content_type = 'image/png'
        elif extension == 'gif':
            content_type = 'image/gif'
        elif extension == 'jpeg' or extension == 'jpg':
            content_type = 'image/jpeg'
        elif extension == 'text' or extension == 'txt':
            content_type = 'text/plain'
        else:
            content_type = 'application/octet-stream'
        content_string = 'Content-Type: ' + content_type + '\r\n'
        self.request.send(content_string.encode('utf8'))

    def sendFile(self, contents):
        self.request.send(('Content-Length: ' + str(len(contents)) + '\r\n').encode('utf8'))
        self.request.send('Connection: close\r\n'.encode('utf8'))
        self.request.send('\r\n'.encode('utf8'))
        self.request.send(contents)

    def handleHTTP(self, text):
        sp = text.split('\r\n')
        request = sp[0].split(' ')
        file_path = '/' + request[1]
        if file_path[0] == '/' and file_path[1] == '/':
            file_path = file_path[1:]
        if file_path == '/':
            file_path = '/index.html'
        file_path = 'Upload' + file_path
        if request[0] == 'GET':
            my_file = Path(file_path)
            if my_file.is_file():
                print("Sending " + file_path)
                try:
                    bbb = my_file.read_bytes()
                    self.sendOK()
                    self.sendContentType(file_path)
                    self.sendFile(bbb)
                except: 
                    self.sendDenied()
            else:
                print("Sending 404, can't find " + file_path)
                self.sendNF()
        else:
            self.sendNF()
        self.request.close()

    def handle(self):
        data = self.request.recv(1024)
        text = data.decode()
        self.handleHTTP(text.strip())


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address):
        socketserver.TCPServer.__init__(self, server_address, RequestHandler)

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 100
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    print("Starting server on port", str(PORT))
    server = Server((HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
