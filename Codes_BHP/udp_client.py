#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

target_host = input("Insert the target: ")
target_port = int(input("Insert the port: "))

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

client.sendto(b">>>", (target_host,target_port))

data, addr = client.recvfrom(4096)
print(data.decode())
client.close()
