import argparse
import socket
import itertools
import string


def generate_password():
    base_list = string.ascii_lowercase + string.digits
    for n in range(1, 5):
        for letters in itertools.product(base_list, repeat=n):
            yield "".join(letters)


class Connect2Server:

    def __init__(self):
        self.description = "Let's connect to a server."
        self.ip_help = "IP address of the server."
        self.port_help = "Connection port."
        self.message_help = "Message sent to server."
        self.parser = None
        self.args = None
        self.password_generator = generate_password()
        self.password = None

    def connect(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('ip_address', help=self.ip_help)
        self.parser.add_argument('port', help=self.port_help)
        self.args = self.parser.parse_args()

        with socket.socket() as client_socket:
            client_socket.connect((self.args.ip_address, int(self.args.port)))
            correct_response = 'Connection success!'
            response = ""
            while response != correct_response:
                self.password = next(self.password_generator)
                client_socket.send(self.password.encode())
                response = client_socket.recv(1024).decode()
            print(self.password)


if __name__ == '__main__':
    Connect2Server().connect()
