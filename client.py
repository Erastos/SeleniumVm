import cmd
import select
import socket
import json
from enum import Enum

commands = {
    "StartBrowser": 0
}


class Client(cmd.Cmd):
    intro = "Welcome to the Selenium Command Console"
    prompt = "[Sel-VM]=> "
    servers = []
    command_buffer = ""
    browser = None

    def preloop(self):
        number_of_servers = int(input("Number of VM's to connect to: "))
        server_addrs = []
        for i in range(1, number_of_servers + 1):
            ip = input(f"Server {i}'s IP Address: ")
            port = int(input(f"Server {i}'s Port Number: "))
            server_addrs.append((ip, port))

        self.servers = list(map(lambda _: socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_addrs))
        for server, addr in zip(self.servers, server_addrs):
            server.connect(addr)

    def postloop(self):
        for server in self.servers:
            server.close()

    def select_inputs(self):
        read_inputs = self.servers.copy()
        write_inputs = []
        exception_inputs = []
        fd_sets = select.select(read_inputs, write_inputs, exception_inputs)
        read_fd_sets = fd_sets[0]
        for socket_server in read_fd_sets:
            print(socket_server.recv(4096).decode('utf-8'))

    @staticmethod
    def create_command(verb, args):
        command_dict = {"verb": verb, "args": args}
        json_string = json.dumps(command_dict)
        return json_string

    def send_command(self, json_string):
        for server in self.servers:
            json_message_encoded = json_string.encode('utf-8')
            server.sendall(f"{len(json_message_encoded)}\r\n".encode('utf-8'))
            # TODO: Check this for errors
            ack = server.recv(4096)
            server.sendall(json_message_encoded)

    def postcmd(self, stop: bool, line: str):
        if not stop:
            self.select_inputs()
        return stop

    def do_startBrowser(self, _):
        json_command = self.create_command(commands["StartBrowser"], None)
        self.send_command(json_command)

    def do_quit(self, _):
        return True

    def do_exit(self, arg):
        return self.do_quit(arg)


if __name__ == '__main__':
    Client().cmdloop()
