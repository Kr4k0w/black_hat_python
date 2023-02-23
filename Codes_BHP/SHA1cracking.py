#!/usr/bin/python

from urllib.request import urlopen;
import hashlib;
hashell = input('Entre com sha1:');

passlist = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt').read(), 'utf-8');



for password in passlist.split('\n'):
    hashguess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest();
    if hashguess == hashell:
        print('[*] A Senha:', str(password));
        quit();
    else:
        print("[-] Senha Guess:", str(password), "A senha não bate, tentando a próxima...");
print("Senha não está na lista!");

