#!/usr/bin/env python3
from binascii import unhexlify
from challenge3 import try_cipher, one_try, get_english_score

# solution
assert b"Now that the party is jumping\n" == one_try(unhexlify("7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f"), b"5")

if __name__ == '__main__':
    results = {}
    for line in open("4.txt"):
        line = line.strip()
        print("Trying to decrypt {}".format(line))
        key, message = try_cipher(unhexlify(line))
        results[get_english_score(message)] = message

    print(results[max(results.keys())].decode())


