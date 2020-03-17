#!/usr/bin/env python3
from base64 import b64decode

ciphers = open("8.txt").read()
keysize = 16


for line_number, line in enumerate(ciphers.splitlines()):
    cipher = b64decode(line.strip())
    chunks = [cipher[i:i + keysize] for i in range(0, len(cipher), keysize)]
    # how many ciphertexts are the same?
    same_chunks = len(chunks) - len(set(chunks))
    if same_chunks > 0:
        print("{} same chunks (line {})".format(same_chunks, line_number))
        assert same_chunks == 3
        assert line_number == 132
