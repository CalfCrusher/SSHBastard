# SSHBastard
**This tool scan CIDR range to search SSH servers, then start to bruteforce every single IP using a given wordlist**

![](https://github.com/CalfCrusher/SSHBastard/blob/main/SSHBastard.png)

### Usage

`$ git clone https://github.com/CalfCrusher/SSHBastard/`

`$ cd SSHBastard && pip3 install -r requirements.txt`

`$ python3 SSHBastard.py 192.168.1.0/24 -u root -f wordlist.txt`

## Disclaimer

This is a tool that i made for learning Python purpose only, it's a slightly modified version of one script from Violent Python book. I rewritten the script using Python 3 and adding CIDR usage. I advise you don't be a twat and don't make anything of illegal. Nowadays try to bruteforce SSH does not make sense at all to me. We're not in '98 and password are not 'password' or '12345' but more complex. Also if you think that on entire internet will be a couple of misconfigured ssh server don't be a looser, bruteforce is always last resort and is not elegant. It makes much more sense to me using this tool as **ssh-honeypot finder**! Again, I'm not responsible for the consequences of illegal use with this tool. Also there're tons of tools better then this.
