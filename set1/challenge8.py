#!/usr/bin/env python3
from base64 import b64decode


def count_duplicate_blocks(cipher: bytes, block_size: int = 16) -> int:
    chunks = [cipher[i:i + block_size] for i in range(0, len(cipher), block_size)]
    return len(chunks) - len(set(chunks))


if __name__ == '__main__':
    ciphers = open("8.txt").read()
    keysize = 16
    for line_number, line in enumerate(ciphers.splitlines()):
        cipher = b64decode(line.strip())
        # how many ciphertexts are the same?
        same_chunks = count_duplicate_blocks(cipher)
        if same_chunks > 0:
            print("{} same chunks (line {})".format(same_chunks, line_number))
            assert same_chunks == 3
            assert line_number == 132
