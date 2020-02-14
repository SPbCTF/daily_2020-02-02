import hashlib
import random

xor = lambda x, y: bytes([a ^ b for (a, b) in zip(x, y)])


def drm_video_encrypt():
    key = bytes(str(random.randint(0, 10**8-1)), 'utf-8')
    plaintext = open("flag.mpeg", "rb").read()
    mask = hashlib.shake_256(key).digest(len(plaintext))
    ciphertext = xor(plaintext, mask)

    with open(f"flag.enc.mpeg", "wb") as w:
        w.write(ciphertext)


if __name__ == "__main__":
    drm_video_encrypt()

