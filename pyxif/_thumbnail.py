"""'exifkeeper' has a function to resize JPEG without losing Exif.
Depend on: PIL, or Pillow
Tested on: 2.7, and 3.4
"""

import io

from PIL import Image
from ._common import *

def thumbnail(data, output, size=(200, 200)):
    """Proportionally Resize without losing Exif.

    thumbnail(data, output, (w, h))
    data: input filename or binary jpeg data(2.x - str, 3.x - bytes)
    output: output filename or instance of io.BytesIO

    This function uses 'PIL.Image.thumbnail' method to resize.
    """

    if data[0:2] == b"\xff\xd8":
        pass
    else:
        with open(data, 'rb') as f:
            data = f.read()

    segments = split_into_segments(data)
    exif = get_exif(segments)

    input_buf = io.BytesIO()
    input_buf.write(data)
    input_buf.seek(0)
    im = Image.open(input_buf)
    im.thumbnail(size, Image.ANTIALIAS)
    if exif is None:
        im.save(output, format="jpeg")
    else:
        im.save(output, format="jpeg", exif=bytes(exif[4:]))