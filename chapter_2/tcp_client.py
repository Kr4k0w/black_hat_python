#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

target_host = input("Insert the target: ")
target_port = int(input("Insert the number of port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host,target_port))

client.send(b"GET / HTTP/1.1\r\nHost:{target_host} \r\n\r\n")

response = client.recv(4096)
print(response.decode())
client.close()
