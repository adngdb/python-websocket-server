#!/usr/bin/env python

import socket
import threading
import config

class WebSocketClient(threading.Thread):
    """
    A single connection (client) of the program
    """
    def __init__(self, sock, addr, server):
        threading.Thread.__init__(self)
        self.s = sock
        self.addr = addr
        self.server = server

    def run(self):
        # Handshaking, create the WebSocket connection
        handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nWebSocket-Origin: http://%s\r\nWebSocket-Location: ws://%s/\r\nWebSocket-Protocol: sample\r\n\r\n" % (config.httphost, config.sockethost)
        self.s.send(handshake)
        data = self.s.recv(1024)

        # Receive and handle data
        while 1:
            data = self.s.recv(1024)
            if not data: break
            print 'Data from', self.addr, ':', data
            self.onreceive(data)

        # Close the client connection
        self.close()

    def close(self):
        """
        Close this connection
        """
        print 'Client closed: ', self.addr
        self.server.remove(self.s)
        self.s.close()

    def send(self, msg):
        """
        Send a message to this client
        """
        msg = '\x00' + msg + '\xff'
        self.s.send(msg)

    def onreceive(self, data):
        """
        Event called when a message is received from this client

        Example:
        Here, send back the received message to all the clients
        """
        data = self._clean(data)
        self.server.send_all(data)

    def _clean(self, msg):
        """
        Remove special chars used for the transmission
        """
        msg = msg.replace('\x00', '', 1)
        msg = msg.replace('\xff', '', 1)
        return msg
