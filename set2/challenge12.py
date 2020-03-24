#!/usr/bin/env python3
import sys
from base64 import b64decode
from binascii import unhexlify, hexlify
import string

sys.path.insert(0, "../set1")
from typing import Tuple
import os
from random import randrange
from challenge7 import ecb_encrypt
from challenge8 import count_duplicate_blocks
from challenge9 import pkcs7_encode
from challenge10 import cbc_encrypt


BLOCK_SIZE = 16

challenge_solution = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


def get_random_bytes(lenth: int = BLOCK_SIZE):
    return os.urandom(lenth)


key = get_random_bytes()


def append() -> bytes:
    return get_random_bytes(randrange(5, 11))


def choose() -> bool:
    return bool(randrange(0, 2))


def append_challenge_solution_and_pad(message: bytes) -> bytes:
    message = message + challenge_solution
    if len(message) % BLOCK_SIZE != 0:
        message = pkcs7_encode(message)
    assert len(message) % BLOCK_SIZE == 0
    return message


def encrypt_with_ecb(message: bytes) -> bytes:
    plain = append_challenge_solution_and_pad(message)
    cipher = ecb_encrypt(plain, key)
    return cipher


def decrypt_one_byte(known_message: bytes) -> bytes:
    brute_force_dict = {}
    pre_prefix = 160
    message_prefix = (BLOCK_SIZE - len(known_message) - 1 + pre_prefix) * b"A"
    #                                                            |  decrypt last byte    |
    #message_prefix round #1:  | 9 blocks 16*A  |    16*A        |  15*A + solution[0]   | solution[1:]
    #message_prefix round #2:  | 9 blocks 16*A  |    16*A        |  14*A + solution[0:2] | solution[2:]
    #message_prefix round #3:  | 9 blocks 16*A  |    16*A        |  13*A + solution[0:3] | solution[3:]

    #                                                                  | decrypt last byte
    #message_prefix round #17: | 9 blocks 16*A  | 15*A + solution[0]   | solution[1:17]
    #message_prefix round #16: | 9 blocks 16*A  | 14*A + solution[0:2] | solution[2:18]
    print(f"{message_prefix=} {len(message_prefix)}")
    for char in string.printable:
        message = message_prefix + known_message + bytes([ord(char)])
        #print(f" {message=} {len(message)}")
        cipher_block = encrypt_with_ecb(message)[pre_prefix:pre_prefix+BLOCK_SIZE]
        brute_force_dict[cipher_block] = message
    
    cipher_test = encrypt_with_ecb(message_prefix)[pre_prefix:pre_prefix+BLOCK_SIZE]
    decrypted_byte = bytes([brute_force_dict[cipher_test][-1]])
    return decrypted_byte



if __name__ == '__main__':
    cipher_16 = encrypt_with_ecb(16 * b"A")
    cipher_17 = encrypt_with_ecb(17 * b"A")
    assert cipher_16[0:16] == cipher_17[0:16]

    plain = b""
    for i in range(40000000):
        decrypted_byte = decrypt_one_byte(plain)
        plain += decrypted_byte
        print(f"{plain=} {len(plain)}")
        if plain == challenge_solution:
            break
    print("done with {}".format(plain.decode()))
    assert plain == challenge_solution
