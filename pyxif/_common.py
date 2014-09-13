import struct

def split_into_segments(data):
    """Slices JPEG meta data into a list from JPEG binary data.
    """
    head = 0
    segments = []

    while 1:
        if data[head: head + 2] == b"\xff\xd8":
            head += 2
        else:
            length = struct.unpack(">H", data[head + 2: head + 4])[0]
            endPoint = head + length + 2
            seg = data[head: endPoint]
            segments.append(seg)
            head = endPoint

        if (head >= len(data)) or (data[head: head + 2] == b"\xff\xda"):
            break

    return segments


def get_exif(segments):
    """Returns Exif from JPEG meta data list
    """
    for seg in segments:
        if seg[0:2] == b"\xff\xe1":
            return seg
    return None