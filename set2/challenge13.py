#/usr/bin/env python3
import sys
sys.path.insert(0, "../set1")
from typing import Dict, List
import os
from binascii import hexlify, unhexlify

from challenge7 import ecb_encrypt, ecb_decrypt
from challenge9 import pkcs7_encode


BLOCK_SIZE = 16

KEY = os.urandom(BLOCK_SIZE)
#KEY = 16 * bytes([12]) # for debugging


def decode(s: str) -> Dict[str, str]:
    d: Dict[str, str] = {}
    for pair in s.split("&"):
        k, v = pair.split("=")
        d[k] = v
    return d


def encode(user: dict) -> str:
    encoded_string = ""
    for k, v in user.items():
        encoded_string += f"&{k}={v}"
    return encoded_string[1:]


def profile_for(email: str):
    email = email.replace("&", "")
    email = email.replace("=", "")
    d = {'email': email,
         'uid': 10,
         'role': 'user',
        }
    return encode(d)


def encrypt_user(profile: str) -> bytes:
    padded_m = pkcs7_encode(profile.encode())
    cipher = ecb_encrypt(padded_m, KEY)
    return cipher


def unpad(m: bytes) -> bytes:
    if m[-1] == BLOCK_SIZE:
        return m
    else:
        # return from index 0 up to x
        # where x is len(m) - (1* m[-1])
        return m[:-m[-1]]


def decrypt_user(cipher: bytes) -> str:
    padded_m = ecb_decrypt(cipher, KEY)
    m = unpad(padded_m).decode()
    return m


assert {'foo': 'bar', 'baz': 'qux', 'zap': 'zazzle'} == decode("foo=bar&baz=qux&zap=zazzle")


def pretty_cipher(cipher: bytes) -> str:
    blocks = [cipher[i:i+BLOCK_SIZE] for i in range(0, len(cipher), BLOCK_SIZE)]
    blocks = [hexlify(block).decode() for block in blocks]
    return " ".join(blocks)


def pretty_plain(plain: str) -> str:
    blocks = [plain[i:i+BLOCK_SIZE].ljust(BLOCK_SIZE*2) for i in range(0, len(plain), BLOCK_SIZE)]
    return " ".join(blocks)


if __name__ == '__main__':
    user_input = "foo@bar.com"
    encoded_user = profile_for(user_input)
    encrypted_user = encrypt_user(encoded_user)
    assert encoded_user == decrypt_user(encrypted_user)

    # challenge
    # given: user_input + encrypt_user/decrypt_user functions including the key
    # challenge: generate an encryped user with the role role=admin

    def e(u):
        u = profile_for(u)
        print(pretty_plain(u))
        c = encrypt_user(u)
        print(pretty_cipher(c))
        return c

    e("foo@bar.com")
    e("foo@bar.co" + 16*"X")
    c1 = e("foooooooooooooooooooo@bar.com")[0:3*BLOCK_SIZE] # < only enc("admin") is missin)
    c2 = e("foo@bar.co" + "admin" + 11 * chr(11))[BLOCK_SIZE:2*BLOCK_SIZE] # 0xb => 11 => len(admin) = 5 => 11 + = 16 = BLOCK_SIZE

    print(pretty_cipher(c1 + c2))
    print(decrypt_user(c1 + c2))
    assert decrypt_user(c1 + c2) == "email=foooooooooooooooooooo@bar.com&uid=10&role=admin"
