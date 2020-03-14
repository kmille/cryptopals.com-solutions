#!/usr/bin/env python
from base64 import b64decode
from Crypto.Cipher import AES

key = "YELLOW SUBMARINE"

cipher = b64decode(open("7.txt").read())
decipher = AES.new(key, AES.MODE_ECB)
message = decipher.decrypt(cipher)
print(message.decode())

# base64 -d 7.txt | openssl enc -aes-128-ecb -d -K $(echo -n "YELLOW SUBMARINE" | xxd -p)
