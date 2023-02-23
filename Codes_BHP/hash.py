#!/usr/bin/python

import hashlib;

hashvalue = input('[*] Enter a string to hash:');

hashhobj1 = hashlib.sha1();
hashhobj1.update(hashvalue.encode());

hashhobj2 = hashlib.md5();
hashhobj2.update(hashvalue.encode());




print("SHA1:",hashhobj1.hexdigest());
print("MD5:", hashhobj2.hexdigest());