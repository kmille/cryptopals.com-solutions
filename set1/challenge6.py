#!/usr/bin/env python3
from typing import List
from base64 import b64decode
from binascii import hexlify

from challenge3 import try_cipher
from challenge5 import repeating_xor


def calc_hamming(a: bytes, b: bytes) -> int:
    assert len(a) == len(b), "{} vs {}".format(len(a), len(b))
    a_bit_string = "".join(["{:08b}".format(x) for x in a])
    b_bit_string = "".join(["{:08b}".format(x) for x in b])
    hamming = 0
    for i in range(len(a_bit_string)):
        if a_bit_string[i] != b_bit_string[i]:
            hamming += 1
    return hamming


assert calc_hamming(b"this is a test", b"wokka wokka!!!"), 4

cipher = b64decode(open("6.txt").read())


def find_keysizes_with_lowest_hamming_distance() -> List[int]:
    dict_keysize_hamming = dict()
    for keysize in range(2, 41):
        chunks = [cipher[i:i + keysize] for i in range(0, len(cipher), keysize)]
        if len(chunks[-1]) != keysize:
            # pad with 0 bytes - not sure if we should do this
            chunks[-1] = chunks[-1] + (keysize - len(chunks[-1])) * bytes([0])
        sum_hamming = 0
        for a in range(len(chunks) - 1):
            sum_hamming += calc_hamming(chunks[a], chunks[a + 1])
        dict_keysize_hamming[sum_hamming / keysize / len(chunks)] = keysize

    smallest_hamming_distances = sorted([x for x in dict_keysize_hamming.keys()])[:3]
    keysizes_with_small_hamming = [dict_keysize_hamming[x] for x in smallest_hamming_distances]
    return keysizes_with_small_hamming


def get_transposed_chunks(keysize) -> List[bytes]:
    chunks_transposed = []
    for i in range(keysize):
        chunks_transposed.append(cipher[i::keysize])
    return chunks_transposed


def get_decrypt_key() -> bytes:
    decrypt_key = bytes()
    for chunk in get_transposed_chunks(find_keysizes_with_lowest_hamming_distance()[0]):
        key, __ = try_cipher(chunk)
        decrypt_key += key
    print("Got decrypt key '{}'".format(decrypt_key.decode()))
    assert decrypt_key == b'Terminator X: Bring the noise'
    return decrypt_key


def decrypt_message() -> None:
    decrypt_key = get_decrypt_key()
    message = repeating_xor(cipher, decrypt_key)
    print(message.decode())


if __name__ == '__main__':
    decrypt_message()

