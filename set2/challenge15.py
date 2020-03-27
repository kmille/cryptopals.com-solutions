#!/usr/bin/env python3
from challenge9 import pkcs7_encode

BLOCK_SIZE = 16


class InvalidPaddingException(Exception):
    pass


def pkcs7_decode(cipher: bytes) -> bytes:
    last_byte = cipher[-1]
    for i in range(last_byte - 1):
        print(f"Comparing {cipher[-i-1]} with {last_byte}")
        if cipher[-i-1] != last_byte:
            raise InvalidPaddingException(f"InvalidPaddingException: got {hex(cipher[-i-1])} should be {hex(last_byte)}")
    print("Padding is valid!")

    return cipher[0:-last_byte]


if __name__ == '__main__':
    #for i in range(100):
    #    pkcs7_decode(pkcs7_encode(i * b"X"))

    pkcs7_decode(b"ICE ICE BABY\x05\x05\x05\x05")
    try:
        pkcs7_decode(b"ICE ICE BABY\x01\x02\x03\x04")
    except InvalidPaddingException as e:
        print(e)
    print("done")
