import argparse
import socket
import itertools
import requests


def get_passwords():
    pw_str = requests.get('https://stepik.org/media/attachments/lesson/255258/passwords.txt').text
    return pw_str.split("\r\n")


class Connect2Server:

    def __init__(self):
        self.description = "Let's connect to a server."
        self.ip_help = "IP address of the server."
        self.port_help = "Connection port."
        self.message_help = "Message sent to server."
        self.parser = None
        self.args = None
        self.password = None
        self.passwords = get_passwords()

    def connect(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('ip_address', help=self.ip_help)
        self.parser.add_argument('port', help=self.port_help)
        self.args = self.parser.parse_args()

        with socket.socket() as client_socket:
            client_socket.connect((self.args.ip_address, int(self.args.port)))
            correct_response = 'Connection success!'
            for pw in self.passwords:
                pw_list = [x.lower() + x.upper() for x in pw]
                pw_combinations = itertools.product(*pw_list)
                for pw_combination in pw_combinations:
                    loc_password = "".join(pw_combination)
                    client_socket.send(loc_password.encode())
                    response = client_socket.recv(1024).decode()
                    if response == correct_response:
                        self.password = loc_password
                        print(self.password)
                        return None


if __name__ == '__main__':
    Connect2Server().connect()
