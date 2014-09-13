#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PIL's image resize manipulation(includes thumbnail function) loses JPEG's.
Helps to transplant Exif data into another JPEG.
Tested on Python 2.7 and 3.4
"""

import io

from _common import *


def transplant(exif_src, image, new_file=""):
    """Transplants exif to another JPEG
    """
    if exif_src[0:2] == b"\xff\xd8":
        src_data = exif_src
    else:
        with open(exif_src, 'rb') as f:
            src_data = f.read()
    segments = split_into_segments(src_data)
    exif = get_exif(segments)
    if exif is None:
        raise ValueError("not found exif in input")

    if image[0:2] == b"\xff\xd8":
        image_data = image
    else:
        with open(image, 'rb') as f:
            image_data = f.read()
    segments = split_into_segments(image_data)
    image_exif = get_exif(segments)

    if image_exif:
        new_data = image_data.replace(image_exif, exif)
    else:
        p = src_data.find(b"\xff\xdb")
        new_data = image_data[0:p] + exif + image_data[p:]

    if isinstance(new_file, io.BytesIO):
        new_file.write(new_data)
        new_file.seek(0)
    elif new_file:
        with open(new_file, "wb+") as f:
            f.write(new_data)
    else:
        with open(image, "wb+") as f:
            f.write(new_data)
