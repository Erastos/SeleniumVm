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
                command_length = conn.recv(4096).decode('utf-8')
                print(repr(command_length))
                command_length = int(command_length.strip())
                assert command_length > 0
                conn.sendall(b"Ack\r\n")
                output = conn.recv(command_length+2).decode('utf-8')
                print(repr(output))
                self.parse_command(output)
            except ConnectionResetError:
                self.client.close()
                break
            conn.send(b"Command Accepted\r\n")

    def parse_command(self, output):
        command_object = json.loads(output)
        if command_object['verb'] == 0 and self.browser is None:
            self.browser = Browser()
        elif command_object['verb'] == 1 and self.browser is not None:
            self.browser.go(command_object['args']['url'])


if __name__ == '__main__':
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.start()
