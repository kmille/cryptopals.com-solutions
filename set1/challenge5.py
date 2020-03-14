#!/usr/bin/env python
from binascii import hexlify

text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"
cipher = b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"


def repeating_xor(plain: bytes, key: bytes) -> bytes:
    cipher = bytes()
    for i, byte in enumerate(plain):
        cipher += bytes([byte ^ key[i % len(key)]])
    return cipher


assert cipher == hexlify(repeating_xor(text.encode(), key))

if __name__ == '__main__':
    my_cipher = repeating_xor(text.encode(), key)
    print(hexlify(my_cipher))
