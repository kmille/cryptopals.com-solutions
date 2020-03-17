#!/usr/bin/env python3
from binascii import unhexlify, hexlify

input_one = unhexlify("1c0111001f010100061a024b53535009181c")
input_two = unhexlify("686974207468652062756c6c277320657965")
result = "746865206b696420646f6e277420706c6179"


def my_xor(a: bytes, b: bytes) -> bytes:
    #print(a, b)
    assert len(a) == len(b)
    output_bytes = bytes()
    for i in range(len(a)):
        output_bytes += bytes([a[i] ^ b[i]])
    return output_bytes


if __name__ == '__main__':
    xored_bytes = my_xor(input_one, input_two)
    assert hexlify(xored_bytes), result
    print(xored_bytes.decode())
