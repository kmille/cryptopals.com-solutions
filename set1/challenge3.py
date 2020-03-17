#!/usr/bin/env python3
from typing import Dict, Tuple
from binascii import unhexlify
import string

from challenge2 import my_xor


def one_try(cipher: bytes, key: bytes) -> bytes:
    xored = my_xor(cipher, (len(cipher) * key))
    #if everything_is_in_ascii_range(xored):
    #    print("possible solution - xored with {} - Result: {}".format(key.decode(), xored.decode()))
    #print("xored with {} - Score: {} - Result: {}".format(key.decode(), get_english_score(xored), xored.decode()))
    return xored


def get_english_score(input_bytes):
    """Compares each input byte to a character frequency 
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language.
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])


def everything_is_in_ascii_range(s: bytes) -> bool:
    for x in s:
        #if b" " not in s:
        #    return False
        if chr(x) not in string.printable:
            return False
    return True


assert b"Cooking MC's like a pound of bacon" == one_try(unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"), b"X")


def try_cipher(cipher: bytes) -> Tuple[bytes, bytes]:
    #alphabet = [x.encode() for x in string.printable]
    alphabet = [bytes([x]) for x in range(256)]
    likelihood_dict: Dict[float, dict] = dict()
    for char in alphabet:
        xored = one_try(cipher, char)
        score = get_english_score(xored)
        likelihood_dict[score] = dict()
        likelihood_dict[score]['xored'] = xored
        likelihood_dict[score]['key'] = char
    winner_score = sorted([x for x in likelihood_dict.keys()], reverse=True)[0]
    #print("Our winner is '{}' with key '{}'".format(likelihood_dict[winner_score]['xored'].decode(), likelihood_dict[winner_score]['key'].decode()))
    print("Our winner is '{}' with key '{}'".format(likelihood_dict[winner_score]['xored'], likelihood_dict[winner_score]['key']))
    return likelihood_dict[winner_score]['key'], likelihood_dict[winner_score]['xored']


if __name__ == '__main__':
    cipher = unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    key, __ = try_cipher(cipher)
    assert key == b"X"

