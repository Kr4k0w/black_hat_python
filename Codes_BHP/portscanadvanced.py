#!/usr/bin/python

# -*- coding: utf-8 -*-

# How to use the advanced port scanner.
#Example of how to use it. ./portscanadvanced.py -H 192.168.1.0 -P 22,135,443,80 

from socket import *; 
import optparse;
from threading import *;

def connScan(tgtHost, tgtPort):
  try:
    sock = socket(AF_INET,SOCK_STREAM);
    sock.connect((tgtHost,tgtPort));
    print('[+]%d/tcp Open' %tgtPort);
  except:
      print('[-] %d/tcp Closed' % tgtPort);
  finally:
    sock.close()

def portScan(tgtHost, tgtPort):
  try:
    tgtIP = gethostbyname(tgtHost);
  except:
    print('Unknown Host %s' %tgtHost);
  try:
    tgtName = gethostbyaddr(tgtIP);
    print('[+] Scan Results for:' + tgtName[0]);
  except:
    print ('[+] Scan Results for:' + tgtIP);
  setdefaulttimeout(1);
  for tgtPort in tgtPort:
    t = Thread(target=connScan, args=(tgtHost, int(tgtPort)));
    t.start()

def main():
  parser = optparse.OptionParser('Usage of Program:' + '-H <target host> -p <target ports> ');
  parser.add_option('-H', dest='tgtHost', type='string', help='specify target host');
  parser.add_option('-P', dest='tgtPort', type='string', help='specify target ports separated by comma');
  (options, args) = parser.parse_args();
  tgtHost = options.tgtHost;
  tgtPorts = str(options.tgtPort).split(',');
  if(tgtHost == None) | (tgtPorts[0] == None):
    print(parser.usage);
    exit(0);
  portScan(tgtHost,tgtPorts);

if __name__ == '__main__':
  main();