#!/usr/bin/env python3
import sys
sys.path.insert(0, "../set1")
from typing import Tuple
from binascii import hexlify, unhexlify
import os
import random
import  string

from challenge7 import ecb_encrypt, ecb_decrypt
from challenge9 import pkcs7_encode

BLOCK_SIZE = 16

KEY = os.urandom(16)
#KEY = os.urandom(16)

len_random = random.randrange(0, 100)
#len_random = 20

challenge = b"THAT IS THE TEXT WE DONT KNOW AND WANT TO ACHIEEEEEEEEEEEEEEEEEEEEEEEEVE!!!!!einself!"


def cipher_has_duplicate_block(cipher: bytes) -> int:
    # idea:  we write x*P + 16*"X" + 16*"X" => how long must be x to get two duplicate cipher blocks?
    # return: index of the first duplicate bock
    blocks = [cipher[i:i+BLOCK_SIZE] for i in range(0, len(cipher), BLOCK_SIZE)]
    for i in range(len(blocks)-1):
        if blocks[i] == blocks[i+1]:
            return i
    return 0


def encrypt(message: bytes, verb: bool = False) -> bytes:
    #AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
    random_prefix = os.urandom(len_random)
    plain = random_prefix + message + challenge
    cipher = ecb_encrypt(pkcs7_encode(plain), KEY)
    if verb:
        print(f"{len(random_prefix)} {random_prefix=} ")
        print("PLAIN  -------------------")
        print(b"     ".join([plain[i:i+BLOCK_SIZE] for i in range(0, len(plain), BLOCK_SIZE)]))
        print("CIPHER -------------------")
        print(b"     ".join([cipher[i:i+BLOCK_SIZE] for i in range(0, len(cipher), BLOCK_SIZE)]))
    return cipher


def calc_len_of_unknown_prefix() -> Tuple[int, int]:
    for i in range(2 * BLOCK_SIZE, 3 * BLOCK_SIZE):
        cipher = encrypt(i*b"X")
        #cipher = encrypt(i*b"X", True)
        #done = cipher_has_duplicate_block(cipher)
        index_of_block_we_can_begin_with = cipher_has_duplicate_block(cipher)
        print("Ciphertext with input of size {} has duplicate cipher block at index {}".format(i, index_of_block_we_can_begin_with))
        if index_of_block_we_can_begin_with > 0:
            fill_chars = i - 2 * BLOCK_SIZE
            print(f"We need {fill_chars} fill bits")
            return index_of_block_we_can_begin_with, fill_chars
    raise Exception("Could not find duplicate blocks")


def oracle(our_first_block: int, fill_chars: int, decrypted_message: bytes) -> bytes:
    padding = (fill_chars + 5*BLOCK_SIZE + (BLOCK_SIZE - 1) - len(decrypted_message)) * "P"
    print(f"{pos=} {padding=}")
    brute_dict = {}
    for char in string.printable:
        message = padding.encode() + decrypted_message + char.encode()
        cipher = encrypt(message)
        cipher_index_one_new_char = (our_first_block + 5) * BLOCK_SIZE
        cipher = cipher[cipher_index_one_new_char: cipher_index_one_new_char + BLOCK_SIZE]
        brute_dict[cipher] = message
    cipher_next_char = encrypt(padding.encode())
    cipher_next_char = cipher_next_char[cipher_index_one_new_char: cipher_index_one_new_char + BLOCK_SIZE]
    try:
        decrypted_byte = bytes([brute_dict[cipher_next_char][-1]])
    except KeyError:
        print("We are done! Stop!")
        return b""
    print(f"Decypted byte {decrypted_byte.decode()}")
    return decrypted_byte


if __name__ == '__main__':
    our_first_block, fill_chars = calc_len_of_unknown_prefix()

    # just for checking the outupt (padding ok?)
    cipher = encrypt(fill_chars * b"P" + b"this is my message which should start on a new block", True)

    decrypted_message = b""
    for pos in range(200):
        decrypted_message += oracle(our_first_block, fill_chars, decrypted_message)
        if challenge == decrypted_message:
            break
    print(decrypted_message)
    assert challenge == decrypted_message
    print("done")
