import hashlib

xor = lambda x, y: bytes([a ^ b for (a, b) in zip(x, y)])


def decrypt():
    key = b"39471025"
    plaintext = open("flag.enc.mpeg", "rb").read()
    mask = hashlib.shake_256(key).digest(len(plaintext))
    ciphertext = xor(plaintext, mask)

    with open(f"flag.dec.mpeg", "wb") as w:
        w.write(ciphertext)


if __name__ == "__main__":
    decrypt()

