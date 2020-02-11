import hashlib
import time
from itertools import chain, product


def bruteforce(charset, maxlength):
    return (bytes(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))


xor = lambda x, y: bytes([a ^ b for (a, b) in zip(x, y)])


def encrypt():
    key = b"39471025"
    plaintext = open("flag.mpeg", "rb").read()
    mask = hashlib.shake_256(key).digest(len(plaintext))
    ciphertext = xor(plaintext, mask)

    with open(f"flag.enc.mpeg", "wb") as w:
        w.write(ciphertext)


def decrypt():
    ciphertext = open("flag.enc.mpeg", "rb").read()

    start_time = time.time()
    for k in bruteforce(b"1234567890", 8):
        msk = hashlib.shake_256(k).digest(4)
        if xor(ciphertext[:len(msk)], msk).startswith(bytes([0, 0, 1, 0xBA])):
            print(f"the key is {k} (for {time.time() - start_time} seconds)")

    print(f"Took {time.time() - start_time} seconds")


if __name__ == "__main__":
    ##encrypt()
    decrypt()

