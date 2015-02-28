import struct


def split_into_segments(data):
    """Slices JPEG meta data into a list from JPEG binary data.
    """
    if data[0:2] != b"\xff\xd8":
        raise ValueError("Given data isn't JPEG.")

    head = 2
    segments = [b"\xff\xd8"]
    while 1:
        if data[head: head + 2] == b"\xff\xda":
            segments.append(data[head:])
            break
        else:
            length = struct.unpack(">H", data[head + 2: head + 4])[0]
            endPoint = head + length + 2
            seg = data[head: endPoint]
            segments.append(seg)
            head = endPoint

        if (head >= len(data)):
            raise ValueError("Wrong JPEG data.")
    return segments


def get_app1(segments):
    """Returns Exif from JPEG meta data list
    """
    for seg in segments:
        if seg[0:2] == b"\xff\xe1":
            return seg
    return None


def merge_segments(segments, exif=b""):
    """Merges Exif with APP0 and APP1 manipulations.
    """
    if segments[1][0:2] == b"\xff\xe0" and segments[2][0:2] == b"\xff\xe1":
        if exif:
            segments[2] = exif
            segments.pop(1)
        elif exif is None:
            segments.pop(2)
        else:
            segments.pop(1)
    elif segments[1][0:2] == b"\xff\xe0":
        if exif:
            segments[1] = exif
    elif segments[1][0:2] == b"\xff\xe1":
        if exif:
            segments[1] = exif
        elif exif is None:
            segments.pop(1)
    else:
        if exif:
            segments.insert(1, exif)
    return b"".join(segments)
