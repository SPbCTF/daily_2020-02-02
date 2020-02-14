#include <iostream>
#include <fstream>
#include <chrono>

#include "lodepng.h"

const unsigned int POINTS = 3, COLORS = 3;


inline unsigned ceil(unsigned a, unsigned b) {
    return (a + b - 1) / b;
}

inline unsigned sqr(int x) {
    return x * x;
}


inline void get_gradient(
        unsigned x, unsigned y,
        unsigned t, unsigned j, unsigned q,
        std::vector<unsigned char>& triangles,
        unsigned w,
        std::vector<unsigned char>& px
        ) {
    std::vector<std::vector<unsigned>> points;

    if ((t + j) % 2 == 0) {
        points = {
                {t * q, 2 * j * q},
                {(t + 1) * q - 1, 2 * (j + 1) * q - 1},
                {(t - 1) * q + 1, 2 * (j + 1) * q - 1}
        };
    } else {
        points = {
                {(t - 1) * q + 1, 2 * j * q},
                {(t + 1) * q - 1, 2 * j * q},
                {t * q, 2 * (j + 1) * q - 1}
        };
    }

    std::vector<unsigned> dists(POINTS);

    for (unsigned i = 0; i < POINTS; i++) {
        dists[i] = sqr(0 + points[i][0] - x) + sqr(0 + points[i][1] - y);
    }

    std::vector<unsigned> products(POINTS, 1);
    unsigned psum = 0;
    for (unsigned i = 0; i < POINTS; i++) {
        for (unsigned k = 0; k < POINTS; k++) {
            if (i == k) {
                continue;
            }

            products[i] *= dists[k];
        }
        psum += products[i];
    }

    std::vector<double> normalized(POINTS);
    for (unsigned i = 0; i < POINTS; i++) {
        normalized[i] = 1.0 * products[i] / std::max(psum, 1u);
    }

    for (unsigned c = 0; c < COLORS; c++) {
        double s = 0;

        for (unsigned i = 0; i < POINTS; i++) {
            s += normalized[i] * triangles[COLORS * POINTS * t + COLORS * i + c];
        }

        px[COLORS * y * w + COLORS * x + c] = (unsigned char) s;
    }
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " source destination" << std::endl;
        return 1;
    }

    std::string src(argv[1]);
    std::string dst(argv[2]);

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    std::ifstream src_file(src, std::ios::in | std::ios::binary);
    std::ofstream dst_file(dst, std::ios::out | std::ios::binary);

    unsigned signature;
    src_file.read((char*)&signature, 4);
    if (signature != 0x494354ff) {
        std::cerr << "Invalid file signature" << std::endl;
        return 1;
    }

    unsigned short q;
    src_file.read((char*)&q, 2);
    unsigned w, h;
    src_file.read((char*)&w, 4);
    src_file.read((char*)&h, 4);

    unsigned lines = ceil(h, 2u * q);
    unsigned blocks = ceil(w, q) + 1;

    std::vector<unsigned char> px(COLORS * w * h);

    for (unsigned j = 0; j < lines; j++) {
        std::vector<unsigned char> triangles(COLORS * POINTS * blocks);
        src_file.read((char*)triangles.data(), COLORS * POINTS * blocks);

        for (unsigned y = 2u * j * q; y < 2 * (j + 1) * q; y++) {
            if (y == h) break;

            for (unsigned x = 0; x < w; x++) {
                unsigned t = x / q, a = x % q, b = y % (2u * q);

                if ((t + j) % 2 == 0) {
                    if (b < 2 * a) {
                        t++;
                    }
                } else {
                    a = q - a;

                    if (b >= 2 * a) {
                        t++;
                    }
                }

                get_gradient(x, y, t, j, q, triangles, w, px);
            }
        }

        /*{
            std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
            std::cerr << "Elapsed " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " mcs"
                      << std::endl;
        }*/
    }

    {
        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        std::cerr << "Elapsed " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " mcs"
                  << std::endl;
    }

    unsigned error = lodepng_encode24_file(dst.c_str(), px.data(), w, h);
    if (error) {
        std::cerr << "PNG encoder error " << error << ": " << lodepng_error_text(error) << std::endl;
        return 1;
    }

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cerr << "Elapsed " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " mcs"
        << std::endl;

    return 0;
}