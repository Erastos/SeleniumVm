#!/usr/bin/env python3

import socket
import json
from socket import AF_INET, SOCK_STREAM
import sys
from browser import Browser


class Server:
    def __init__(self, host, port):
        self.client = None
        self.port = port
        self.browser = None
        self.host = host
        self.createClient()

    def createClient(self):
        self.client = socket.socket(AF_INET, SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind((self.host, self.port))

    def start(self):
        self.client.listen()
        print(f"Server Started on {self.host}:{self.port}")
        conn, addr = self.client.accept()
        print(f"Accepted Connection from {addr}")
        while True:
            try:
                message = self.retrieve_message(conn)
                print(message)
                self.parse_command(message)
            except ConnectionResetError:
                self.client.close()
                break
            conn.send(b"Command Accepted\r\n")

    @staticmethod
    def retrieve_message(self, conn):
        counter = 0
        message = ""
        while counter < 1:
            partial_message = conn.recv(256).decode('utf-8')
            for c in partial_message:
                message += c
                if c == '\n':
                    counter += 1
        return message

    def parse_command(self, output):
        command_object = json.loads(output)
        if command_object['verb'] == 0 and self.browser is None:
            self.browser = Browser()
        elif command_object['verb'] == 1 and self.browser is not None:
            self.browser.go(command_object['args']['url'])


if __name__ == '__main__':
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.start()
