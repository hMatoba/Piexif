"""PIL's image resize manipulation(includes thumbnail function) loses JPEG's.
Helps to transplant Exif data into another JPEG.
Tested on Python 2.7 and 3.4
"""

import io

from ._common import *


def remove(src, new_file=""):
    """Removes exif.
    remove(src, new_file[optional])
    src - filename or JPEG data(2.7 - str, 3.4 - bytes)
    When "new_file" is not given, src is overwritten.
    """
    if src[0:2] == b"\xff\xd8":
        src_data = src
    else:
        with open(src, 'rb') as f:
            src_data = f.read()
    segments = split_into_segments(src_data)
    exif = get_exif(segments)

    if exif:
        new_data = src_data.replace(exif, b"")
    else:
        new_data = src_data

    if isinstance(new_file, io.BytesIO):
        new_file.write(new_data)
        new_file.seek(0)
    elif new_file:
        with open(new_file, "wb+") as f:
            f.write(new_data)
    else:
        with open(src, "wb+") as f:
            f.write(new_data)
