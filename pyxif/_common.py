import io
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


def get_exif(segments):
    """Returns Exif from JPEG meta data list
    """
    for seg in segments:
        if seg[0:2] == b"\xff\xe1":
            return seg
    return None


def merge_segments(segments, exif=b""):
    o = io.BytesIO()
    for seg in segments:
        if seg[0:2] == b"\xff\xe0":
            if exif:
                pass
            else:
                o.write(seg)
        elif seg[0:2] == b"\xff\xe1":
            if exif:
                o.write(exif)
            elif exif is None:
                pass
            else:
                o.write(seg)
        else:
            o.write(seg)
    o.seek(0)
    return o.getvalue()
