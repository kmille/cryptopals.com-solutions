#!/usr/bin/env python3
from base64 import b64decode
from Crypto.Cipher import AES

key = b"YELLOW SUBMARINE"

if __name__ == '__main__':
    cipher = b64decode(open("7.txt").read())
    decipher = AES.new(key, AES.MODE_ECB)
    message = decipher.decrypt(cipher)
    print(message.decode())
    assert message[:33] == b"I'm back and I'm ringin' the bell"

# base64 -d 7.txt | openssl enc -aes-128-ecb -d -K $(echo -n "YELLOW SUBMARINE" | xxd -p)
