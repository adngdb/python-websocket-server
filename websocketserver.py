#!/usr/bin/env python

import socket
import threading
import config
import websocketclient

class WebSocketServer:
    """
    Handle the Server, bind and accept new connections, open and close
    clients connections.
    """
    def __init__(self):
        self.clients = []

    def start(self):
        """
        Start the server.
        """
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', config.socketport))
        s.listen(1)

        try:
            while 1:
                conn, addr = s.accept()
                print('Connected by', addr)
                newClient = websocketclient.WebSocketClient(conn, addr, self)
                self.clients.append(newClient)
                newClient.start()
        except KeyboardInterrupt:
            [client.close() for client in self.clients]
            s.close()

    def send_all(self, data):
        """
        Send a message to all the currenly connected clients.
        """
        [client.send(data) for client in self.clients]

    def remove(self, client):
        """
        Remove a client from the connected list.
        """
        l = threading.Lock()
        l.acquire()
        self.clients.remove(client)
        l.release()
