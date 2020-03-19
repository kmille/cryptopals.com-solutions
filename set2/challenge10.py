#!/usr/bin/env python3
import sys
sys.path.insert(0, "../set1")
from base64 import b64decode
from challenge7 import ecb_decrypt, ecb_encrypt
from challenge2 import my_xor as xor


def cbc_decrypt(cipher_text: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
    assert len(cipher_text) % block_size == 0
    blocks = [cipher_text[x: x+block_size] for x in range(0, len(cipher_text), block_size)]
    message = b""
    for block in blocks:
        intermediate = ecb_decrypt(block, key)
        plain = xor(intermediate, iv)
        iv = block
        message += plain
    return message


def cbc_encrypt(message: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
    assert len(message) % block_size == 0
    blocks = [message[x: x+block_size] for x in range(0, len(message), block_size)]
    cipher = b""
    for block in blocks:
        intermediate = xor(block, iv)
        cipher_block = ecb_encrypt(intermediate, key)
        cipher += cipher_block
        iv = cipher_block
    return cipher


if __name__ == '__main__':
    cipher = b64decode(open("10.txt", "rb").read())
    key = b"YELLOW SUBMARINE"
    iv = bytes(16 * [0])
    message = cbc_decrypt(cipher, key, iv)
    assert message[:33] == b"I'm back and I'm ringin' the bell"
    print(message.decode())
    assert cipher == cbc_encrypt(message, key, iv)
    print("done")
