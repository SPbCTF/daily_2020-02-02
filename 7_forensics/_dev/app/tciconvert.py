#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PIL.Image
import subprocess
import struct

PIL.Image.MAX_IMAGE_PIXELS = 1668 * 768
LINE_LIMIT = 768


def ceil(a, b):
    return (a + b - 1) // b


def get_color(im, px, dot):
    w, h = im.size

    if 0 <= dot[0] < w and 0 <= dot[1] < h:
        return (px[dot] * 3)[:3]
    else:
        return 0, 0, 0


def get_dots(i, j, q):
    # clockwise order, starting from top-left
    return [
        (i * q, 2 * j * q),
        ((i + 1) * q - 1, 2 * (j + 1) * q - 1),
        ((i - 1) * q + 1, 2 * (j + 1) * q - 1)
    ] if (i + j) % 2 == 0 else [
        ((i - 1) * q + 1, 2 * j * q),
        ((i + 1) * q - 1, 2 * j * q),
        (i * q, 2 * (j + 1) * q - 1)
    ]


def encode(src, dst, q=5, enforce_limits=True):
    im = PIL.Image.open(src).convert("RGB")
    px = im.load()

    w, h = im.size
    if enforce_limits and (w >= LINE_LIMIT or h >= LINE_LIMIT):
        raise ValueError("Too huge image")

    w, h = im.size

    lines = ceil(h, 2 * q)
    blocks = ceil(w, q) + 1

    with open(dst, "wb") as f:
        f.write(b"\xffTCI")
        f.write(struct.pack("<HII", q, w, h))

        for j in range(lines):
            for i in range(blocks):
                dots = get_dots(i, j, q)
                for dot in dots:
                    f.write(struct.pack("<BBB", *get_color(im, px, dot)))


def dist2(src, dst):
    return sum(
        (a - b) ** 2
        for a, b in zip(src, dst)
    )


def get_gradient(point, border, colors):
    dists = [dist2(point, dst) for dst in border]
    products = []

    for i in range(len(border)):
        p = 1
        for j in range(len(border)):
            if i == j:
                continue
            p *= dists[j]
        products.append(p)

    normalized = [
        p / max(sum(products), 1)
        for p in products
    ]

    return tuple(
        int(sum([coef * comp for coef, comp in zip(normalized, component)]))
        for component in zip(*colors)
    )


def decode_legacy(src, dst):
    with open(src, "rb") as f:
        signature = f.read(4)
        assert(signature == b"\xffTCI")

        q, w, h = struct.unpack("<HII", f.read(10))

        lines = ceil(h, 2 * q)
        blocks = ceil(w, q) + 1

        data = list(struct.iter_unpack("<BBB", f.read()))

        assert(len(data) == lines * blocks * 3)

        color = iter(data)

        im = PIL.Image.new("RGB", (w, h))
        px = im.load()

        for j in range(lines):
            triangles = [
                tuple(next(color) for _ in range(3))
                for _ in range(blocks)
            ]

            for y in range(2 * j * q, min(2 * (j + 1) * q, h)):
                for x in range(0, w):
                    t = x // q

                    if (t + j) % 2 == 0:
                        a = x % q
                        b = y % (2 * q)

                        if b < 2 * a:
                            t += 1
                    else:
                        a = q - x % q
                        b = y % (2 * q)

                        if b >= 2 * a:
                            t += 1

                    px[x, y] = get_gradient((x, y), get_dots(t, j, q), triangles[t])

        im.save(dst)


def decode(src, dst):
    subprocess.run(
        ["drawer/drawer", src, dst]
    )


if __name__ == "__main__":
    import sys
    import time

    start = time.time()

    src = sys.argv[1]
    quality = 10 if len(sys.argv) < 3 else int(sys.argv[2])

    prefix = src[:src.rfind(".")]

    dst = f"{prefix}.tci" if len(sys.argv) < 4 else sys.argv[3]
    dec = f"{prefix}.decoded.png" if len(sys.argv) < 5 else sys.argv[4]

    encode(src, dst, quality, False)
    decode(dst, dec)

    print("Converted in", time.time() - start, "seconds")
