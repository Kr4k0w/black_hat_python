#!/usr/bin/python

import ftplib;

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname);
        ftp.login('anonymous','anonymous');
        print("[*]", hostname, 'Login anonimo FTP sucedido.');
        ftp.quit()
        return True
    except (Exception, e):
        print("[-]", hostname, "Login anonimo FTP falho.");

host = input("Entre com o endereço IP:");
anonLogin(host);
