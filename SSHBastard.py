# This tool scan a choosen network to search ssh servers on port 22
# and port 2222 (a classic). Then will try to brute them.
# It's a tool that i made for learning python purpose only.
# Nowadays bruteforcing SSH is does not make sense at all to me.
# We're not in '98 and password are not 'password' or '12345' but more complex.
# Also if you think that on entire internet will be a couple of misconfigured
# ssh server don't loose your time. Keep studying and coding.

import os

from pexpect import pxssh


def send_command(s, cmd):
    """Function to send commands to remote server"""

    s.sendline(cmd)
    s.prompt()
    print(s.before)

def connect(host, user, password):
    """Function to connect to server and try to login"""

    try:
        s = pxssh.pxssh()
        s.force_password = True
        s.login(host, user, password)
        return s
    except pxssh.ExceptionPxssh as e:
        print('[!] Failed to login')
        print(e)

def main():
    """Main function of tool"""

    host = "31.193.129.219"
    user = "chris"
    password = "jkshdfiDFFFuahsfs90f90sdyf"
    connection = connect(host, user, password)
    send_command(connection, 'whoami')


if __name__ == "__main__":
    os.system('clear')
    main()
