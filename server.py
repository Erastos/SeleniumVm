import socket
from socket import AF_INET, SOCK_STREAM
import sys

HOST = "127.0.0.1"


class Server:
    def __init__(self, port):
        self.client = None
        self.port = port
        self.createClient()

    def createClient(self):
        self.client = socket.socket(AF_INET, SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind((HOST, self.port))

    def start(self):
        self.client.listen()
        print(f"Server Started on {HOST}:{self.port}")
        conn, addr = self.client.accept()
        print(f"Accepted Connection from {addr}")
        while True:
            conn.send(b"Connection Received\r\n")
            try:
                command_length = conn.recv(4096)
                assert command_length > 0
                conn.sendall(b"Ack\r\n")
                output = conn.recv(command_length).decode('utf-8')
                print(output)
            except ConnectionResetError:
                self.client.close()
                break
            conn.send(b"Command Accepted\r\n")


if __name__ == '__main__':
    server = Server(int(sys.argv[1]))
    server.start()
