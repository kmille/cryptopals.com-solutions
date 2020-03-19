#!/usr/bin/env python3
from base64 import b64decode
from Crypto.Cipher import AES


def ecb_decrypt(cipher_text: bytes, key: bytes) -> bytes:
    assert len(key) % 16 == 0
    decipher = AES.new(key, AES.MODE_ECB)
    message = decipher.decrypt(cipher_text)
    return message


def ecb_encrypt(message: bytes, key: bytes) -> bytes:
    assert len(key) % 16 == 0
    crypter = AES.new(key, AES.MODE_ECB)
    cipher = crypter.encrypt(message)
    return cipher


if __name__ == '__main__':
    cipher = b64decode(open("7.txt").read())
    key = b"YELLOW SUBMARINE"
    message = ecb_decrypt(cipher, key)
    print(message.decode())
    assert message[:33] == b"I'm back and I'm ringin' the bell"
    assert cipher == ecb_encrypt(message, key)
    print("done")

# base64 -d 7.txt | openssl enc -aes-128-ecb -d -K $(echo -n "YELLOW SUBMARINE" | xxd -p)
