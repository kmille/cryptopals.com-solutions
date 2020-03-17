#!/usr/bin/env python3
from binascii import unhexlify
from base64 import b64encode

#  https://www.lucidchart.com/techblog/2017/10/23/base64-encoding-a-visual-explanation/

input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
output_string = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

#s = unhexlify(input_string)
#print(s.decode())
#s2 = b64encode(s)
#print(s2.decode())
#assert s2.decode(), output_string


def my_unhexlify(inbut):
    assert len(inbut) % 2 == 0
    output = ""
    for i in range(0, len(inbut), 2):
        byte_string = inbut[i:i+2]
        output += chr(int(byte_string, 16))
    #print(output)
    return output


def my_b64encode(inbut):
    b64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    assert len(b64_alphabet) == 64
    bit_string = ""
    for char in inbut:
        bit_string += "{0:08b}".format(ord(char))
    if len(bit_string) % 6 != 0:
        bit_string += (6 - (len(bit_string) % 6)) * "0"
    base64_encoded_output = ""
    for i in range(0, len(bit_string), 6):
        base64_encoded_output += b64_alphabet[int(bit_string[i:i+6], 2)]
    base64_encoded_output += (3 - (len(inbut) % 3)) * "="
    #print(bit_string)
    #print(base64_encoded_output)
    return base64_encoded_output

assert my_b64encode("a"), "YQ=="

if __name__ == '__main__':
    print("input: {}".format(input_string))
    s = my_unhexlify(input_string)
    print("unhexlify: {}".format(s))
    s2 = my_b64encode(s)
    print("base64:: {}".format(s2))
    assert s2, output_string

    print("done")

