#!/usr/bin/env python
from binascii import unhexlify
import string

from challenge2 import my_xor


from ipdb import set_trace


def one_try(cipher: bytes, key: bytes) -> bytes:
    xored = my_xor(cipher, (len(cipher) * key))
    if everything_is_in_ascii_range(xored):
        print("possible solution - xored with {} - Result: {}".format(key.decode(), xored.decode()))
    return xored


def everything_is_in_ascii_range(s: bytes) -> bool:
    for x in s:
        if b" " not in s:
            return False
        if chr(x) not in string.printable:
            return False
    return True


assert b"Cooking MC's like a pound of bacon" == one_try(unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"), b"X")


def try_cipher(cipher: bytes) -> None:
    #alphabet = [x.encode() for x in string.printable]
    alphabet = [bytes([x]) for x in list(range(256))]
    for char in alphabet:
        one_try(cipher, char)


if __name__ == '__main__':
    cipher = unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    try_cipher(cipher)


