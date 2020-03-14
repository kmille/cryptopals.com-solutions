#!/usr/bin/env python
from binascii import unhexlify
import string

from challenge2 import my_xor


from ipdb import set_trace

cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def one_try(cipher, key):
    return my_xor(cipher, (len(cipher) * key).encode())


def everything_is_in_ascii_range(s):
    for x in s:
        # remove \r and \n
        if chr(x) not in string.printable[:-5]:
            return False
    return True

assert b"Cooking MC's like a pound of bacon" == one_try(unhexlify(cipher), "X")

for char in string.printable:
    xored = one_try(unhexlify(cipher), char)
    if everything_is_in_ascii_range(xored):
        print("possible solution - xored with {} - Result: {}".format(char, xored.decode()))


