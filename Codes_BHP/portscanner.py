#!/usr/bin/python

import socket;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
socket.setdefaulttimeout(3);

host = (input("Insert the host:")); 
port = int(input("Insert the port:"));

def portscanner(port):
  if sock.connect_ex((host,port)):
    print("Port %d is closed" % (port) );
  else:
      print("Port %d is opened" % (port));
portscanner(port);
