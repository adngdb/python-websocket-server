#!/usr/bin/env python

import socket
import threading
import config
import websocketclient

class WebSocketServer:
    def __init__(self):
        self.clients = []

    def start(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', config.socketport))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            print 'Connected by', addr
            self.clients.append(conn)
            websocketclient.WebSocketClient(conn, addr, self).start()

    def send_all(self, data):
        data = '\x00' + data + '\xff'
        [conn.send(data) for conn in self.clients]

    def remove(self, client):
        l = threading.Lock()
        l.acquire()
        self.clients.remove(client)
        l.release()
