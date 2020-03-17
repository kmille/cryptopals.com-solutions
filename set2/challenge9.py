#!/usr/bin/env python3


def pkcs7_encode(message: bytes, block_size: int = 16) -> bytes:
    remainder = block_size % len(message)
    encoded_message = message + bytes(remainder * [remainder])
    return encoded_message


if __name__ == '__main__':
    m = b"this is a test"
    encoded_m = pkcs7_encode(m)
    print(encoded_m)
    assert encoded_m == b"this is a test\x02\x02"

