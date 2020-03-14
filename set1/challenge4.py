#!/usr/bin/env python
from binascii import unhexlify
from challenge3 import try_cipher, one_try

from ipdb import set_trace

# solution
assert b"Now that the party is jumping\n" == one_try(unhexlify("7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f"), b"5")

if __name__ == '__main__':
    for line in open("4.txt"):
        line = line.strip()
        print("Trying to decrypt {}".format(line))
        try_cipher(unhexlify(line))
