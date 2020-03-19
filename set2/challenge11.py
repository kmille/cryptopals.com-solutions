#!/usr/bin/env python3
import sys
sys.path.insert(0, "../set1")
from typing import Tuple
import os
from random import randrange
from challenge7 import ecb_encrypt
from challenge8 import count_duplicate_blocks
from challenge9 import pkcs7_encode
from challenge10 import cbc_encrypt

BLOCK_SIZE = 16


def get_random_bytes(lenth: int = BLOCK_SIZE):
    return os.urandom(lenth)


def append() -> bytes:
    return get_random_bytes(randrange(5, 11))


def choose() -> bool:
    return bool(randrange(0, 2))


def build_message(message: bytes) -> bytes:
    message_prefix = append()
    message_suffix = append()
    message = message_prefix + message + message_suffix
    if len(message) % BLOCK_SIZE != 0:
        message = pkcs7_encode(message)
    assert len(message) % BLOCK_SIZE == 0
    return message


def encrypt_message(message: bytes) -> Tuple[str, bytes]:
    message = build_message(message)
    key = get_random_bytes()
    if choose():
        # use cbc
        mode = "cbc"
        iv = get_random_bytes()
        cipher = cbc_encrypt(message, key, iv)
    else:
        mode = "ecb"
        cipher = ecb_encrypt(message, key)
    return mode, cipher


if __name__ == '__main__':
    ciphers = [encrypt_message(bytes(100)) for __ in range(20)]
    ciphers = sorted(ciphers, key=lambda x: x[0])
    for (mode, cipher) in ciphers:
        if count_duplicate_blocks(cipher) > 0:
            assert mode == "ecb"
        else:
            assert mode == "cbc"
    print("done")
