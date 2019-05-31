import argparse
import glob
import numpy as np

from itertools import combinations
from PIL import Image


def _average_hashing(img, hash_size):
    _size = int(np.sqrt(hash_size))
    img = img.resize((_size, _size), Image.ANTIALIAS)
    img = img.convert('L')

    pix_data = list(img.getdata())
    avg_pix = sum(pix_data) / len(pix_data)

    res = ['1' if pix >= avg_pix else '0' for pix in pix_data]
    res = ''.join(res)
    hex_res = str(hex(int(res, 2)))[2:][::-1].upper()

    return hex_res


def hamming_distance(img0, img1):
    res = [1 if i != j else 0 for i, j in zip(img0, img1)]

    return sum(res)


def Matcher(path, hash_size=64):
    res = []
    images = {image: Image.open(image) for image in glob.glob(path)}

    for image0, image1 in combinations(images.keys(), 2):
        hex0 = _average_hashing(images[image0], hash_size=hash_size)
        hex1 = _average_hashing(images[image1], hash_size=hash_size)

        if hamming_distance(hex0, hex1) == 0:
            res.extend([image0, image1])
    for im in set(res):
        print(im)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Search for duplicated & modified images',
    )
    parser.add_argument(
        '--path',
        type=str,
        help='Path to directory w/ pics',
        required=True,
    )
    parser.add_argument(
        '--hash_size',
        type=int,
        help='Hashing size',
        default=64,
    )
    args = parser.parse_args()
    Matcher(args.path+'/*', args.hash_size)
