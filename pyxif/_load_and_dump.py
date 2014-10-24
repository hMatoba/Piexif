"""EXIF is a set of several IFDs.
Oth IFD can include "Make", "Model" and more...
Exif IFD can include "ExposureTime", "ISOSpeed" and more...
GPS IFD can include GPS information.

Pass dict(s), that shows several IFD, to "dump" function.
exifbytes = pyxif.dump(0th_dict, exif_dict, gps_dict) # second and third are optional.

To use dict as IFD data, it needs...
  A tag number means which property? - 256: ImageWidth, 272: Model...
  Appropriate type for property. - long for ImageWidth, str for Model...
    zeroth_ifd = {pyxif.ImageGroup.Make: "Canon",
                  pyxif.ImageGroup.XResolution: (96, 1),
                  pyxif.ImageGroup.YResolution: (96, 1),
                  pyxif.ImageGroup.Software: "Photoshop x.x.x",
                  }

Property name and tag number
  For 0th IFD - under "pyxif.ImageGroup"
  For Exif IFD - under "pyxif.PhotoGroup"
  For GPS IFD - under "pyxif.GPSInfoGroup"

Property and appropriate type
  See variable"TAGS" in this script.

"Byte": int
"Ascii": str
"Short": int
"Long": Long
"Rational": (long, long)
"Undefined": str
"SLong": long
"SRational": (long, long)
"""

import io
import struct

from ._common import *
from ._exif import *



TYPES = {
    "Byte": 1,
    "Ascii": 2,
    "Short": 3,
    "Long": 4,
    "Rational": 5,
    "Undefined": 7,
    "SLong": 9,
    "SRational": 10}


POINTERS = (34665, 34853)


LITTLE_ENDIAN = b"\x49\x49"


TIFF_HEADER_LENGTH = 8


class ExifReader(object):
    def __init__(self, data):
        if data[0:2] == b"\xff\xd8":
            pass
        else:
            with open(data, 'rb') as f:
                data = f.read()

        segments = split_into_segments(data)
        exif = get_exif(segments)

        if exif:
            self.exif_str = exif[10:]
            endian = self.exif_str[0:2]
            if endian  == LITTLE_ENDIAN:
                self.endian_mark = "<"
            else:
                self.endian_mark = ">"
        else:
            self.exif_str = None

    def get_exif_ifd(self):
        exif_dict = {}
        gps_dict = {}

        pointer = struct.unpack(self.endian_mark + "L", self.exif_str[4:8])[0]
        zeroth_dict = self.get_ifd_dict(pointer)

        if 34665 in zeroth_dict:
            pointer = struct.unpack(self.endian_mark + "L", zeroth_dict[34665][2])[0]
            exif_dict = self.get_ifd_dict(pointer)

        if 34853 in zeroth_dict:
            pointer = struct.unpack(self.endian_mark + "L", zeroth_dict[34853][2])[0]
            gps_dict = self.get_ifd_dict(pointer)

        return zeroth_dict, exif_dict, gps_dict

    def get_ifd_dict(self, pointer):
        ifd_dict = {}
        tag_count = struct.unpack(self.endian_mark + "H", self.exif_str[pointer: pointer+2])[0]
        offset = pointer + 2
        for x in range(tag_count):
            pointer = offset + 12 * x
            tag_code = struct.unpack(self.endian_mark + "H", self.exif_str[pointer: pointer+2])[0]
            value_type = struct.unpack(self.endian_mark + "H", self.exif_str[pointer + 2: pointer + 4])[0]
            value_num = struct.unpack(self.endian_mark + "L", self.exif_str[pointer + 4: pointer + 8])[0]
            value = self.exif_str[pointer+8: pointer+12]
##            print(tag_code, [value_type, value_num, value])
            ifd_dict.update({tag_code:[value_type, value_num, value]})
        return ifd_dict

    def get_info(self, val):
        data = None

        if val[0] == 1: # BYTE
            if not isinstance(val[2][0], int):
                data = int(val[2][0].encode("hex"), 16)
            else:
                data = val[2][0]
        elif val[0] == 2: # ASCII
            if val[1] > 4:
                pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
                data = self.exif_str[pointer: pointer+val[1] - 1]
            else:
                data = val[2][0: val[1] - 1]
            try:
                data = data.decode()
            except:
                pass
        elif val[0] == 3: # SHORT
            data = struct.unpack(self.endian_mark + "H", val[2][0:2])[0]
        elif val[0] == 4: # LONG
            data = struct.unpack(self.endian_mark + "L", val[2])[0]
        elif val[0] == 5: # RATIONAL
            pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
            length = val[1]
            if length > 1:
                data = tuple(
                    (struct.unpack(self.endian_mark + "L", self.exif_str[pointer + x * 8: pointer + 4 + x * 8])[0],
                     struct.unpack(self.endian_mark + "L", self.exif_str[pointer + 4 + x * 8: pointer + 8 + x * 8])[0])
                    for x in range(val[1])
                )
            else:
                data = (struct.unpack(self.endian_mark + "L", self.exif_str[pointer: pointer + 4])[0],
                        struct.unpack(self.endian_mark + "L", self.exif_str[pointer + 4: pointer + 8])[0])
        elif val[0] == 7: # UNDEFINED BYTES
            if val[1] > 4:
                pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
                data = self.exif_str[pointer: pointer+val[1]]
            else:
                data = val[2][0: val[1]]
        elif val[0] == 9: # SLONG
            data = struct.unpack(self.endian_mark + "l", val[2])[0]
        elif val[0] == 10: # SRATIONAL
            pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
            data = (struct.unpack(self.endian_mark + "l", self.exif_str[pointer: pointer + 4])[0],
                    struct.unpack(self.endian_mark + "l", self.exif_str[pointer + 4: pointer + 8])[0])

        return data


def load(input_data):
    r"""converts exif bytes to dicts
    zeroth_dict, exif_dict, gps_dict = pyxif.load(input_data)
    input_data - filename or JPEG data(b"\xff\xd8......")
    """
    exifReader = ExifReader(input_data)
    if exifReader.exif_str is None:
        return {}, {}, {}
    zeroth_ifd, exif_ifd, gps_ifd = exifReader.get_exif_ifd()
    zeroth_dict = {key: (TAGS["Image"][key]["name"], exifReader.get_info(zeroth_ifd[key]))
                   for key in zeroth_ifd if key in TAGS["Image"]}
    exif_dict = {key: (TAGS["Photo"][key]["name"], exifReader.get_info(exif_ifd[key]))
                 for key in exif_ifd if key in TAGS["Photo"]}
    gps_dict = {key: (TAGS["GPSInfo"][key]["name"], exifReader.get_info(gps_ifd[key]))
                for key in gps_ifd if key in TAGS["GPSInfo"]}

    return zeroth_dict, exif_dict, gps_dict


def dump(zeroth_ifd, exif_ifd={}, gps_ifd={}):
    """converts dict to exif bytes
    exif_bytes = pyxif.dump(zeroth_ifd, exif_ifd[optional], gps_ifd[optional])
    zeroth_ifd - dict of 0th IFD
    exif_ifd - dict of Exif IFD
    gps_ifd - dict of GPS IFD
    """
    header = b"\x45\x78\x69\x66\x00\x00\x4d\x4d\x00\x2a\x00\x00\x00\x08"
    exif_is = False
    gps_is = False
    if len(exif_ifd):
        zeroth_ifd.update({34665: 1})
        exif_is = True
    if len(gps_ifd):
        zeroth_ifd.update({34853: 1})
        gps_is = True

    zeroth_set = dict_to_bytes(zeroth_ifd, "Image", 0)
    zeroth_length = len(zeroth_set[0]) + exif_is * 12 + gps_is * 12 + 4 + len(zeroth_set[1])

    if exif_is:
        exif_set = dict_to_bytes(exif_ifd, "Photo", zeroth_length)
        exif_bytes = b"".join(exif_set)
        exif_length = len(exif_bytes)
    else:
        exif_bytes = b""
        exif_length = 0
    if gps_is:
        gps_set = dict_to_bytes(gps_ifd, "GPSInfo", zeroth_length + exif_length)
        gps_bytes = b"".join(gps_set)
        gps_length = len(gps_bytes)
    else:
        gps_bytes = b""
        gps_length = 0

    if exif_is:
        pointer_value = TIFF_HEADER_LENGTH + zeroth_length
        pointer_str = struct.pack(">I", pointer_value)
        key = 34665
        key_str = struct.pack(">H", key)
        type_str = struct.pack(">H", TYPES["Long"])
        length_str = struct.pack(">I", 1)
        exif_pointer = key_str + type_str + length_str + pointer_str
    else:
        exif_pointer = b""
    if gps_is:
        pointer_value = TIFF_HEADER_LENGTH + zeroth_length + exif_length
        pointer_str = struct.pack(">I", pointer_value)
        key = 34853
        key_str = struct.pack(">H", key)
        type_str = struct.pack(">H", TYPES["Long"])
        length_str = struct.pack(">I", 1)
        gps_pointer = key_str + type_str + length_str + pointer_str
    else:
        gps_pointer = b""
    zeroth_bytes = zeroth_set[0] + exif_pointer + gps_pointer + b"\x00\x00\x00\x00" + zeroth_set[1]

    return header + zeroth_bytes + exif_bytes + gps_bytes


def dict_to_bytes(ifd_dict, group, ifd_offset):
    exif_ifd_is = False
    gps_ifd_is = False
    tag_count = len(ifd_dict)
    entry_header = struct.pack(">H", tag_count)
    if group == "Image":
        entries_length = 2 + tag_count * 12 + 4
    else:
        entries_length = 2 + tag_count * 12
    entries = b""
    values = b""

    for n, key in enumerate(sorted(ifd_dict)):
        if key == 34665:
            exif_ifd_is = True
            continue
        elif key == 34853:
            gps_ifd_is = True
            continue

        raw_value = ifd_dict[key]
        key_str = struct.pack(">H", key)
        value_type = TAGS[group][key]["type"]
        type_str = struct.pack(">H", TYPES[value_type])
        if value_type == "Byte":
            length = 1
            value_str = struct.pack('>B', raw_value)[0:1] + b"\x00" * 3
        elif value_type == "Short":
            length = 2
            value_str = struct.pack('>H', raw_value)[0:2] + b"\x00" * 2
        elif value_type == "Long":
            length = 1
            value_str = struct.pack('>L', raw_value)
        elif value_type == "SLong":
            length = 1
            value_str = struct.pack('>l', raw_value)
        elif value_type == "Ascii":
            new_value = raw_value.encode() + b"\x00"
            length = len(new_value)
            if length > 4:
                offset = (TIFF_HEADER_LENGTH + ifd_offset +
                          entries_length + len(values))
                value_str = struct.pack(">I", offset)
                values += new_value
            else:
                value_str = new_value + b"\x00" * (4 - length)
        elif value_type == "Rational":
            length = 1
            num, den = raw_value
            new_value = struct.pack(">L", num) + struct.pack(">L", den)
            offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
            value_str = struct.pack(">I", offset)
            values += new_value
        elif value_type == "SRational":
            length = 1
            num, den = raw_value
            new_value = struct.pack(">l", num) + struct.pack(">l", den)
            offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
            value_str = struct.pack(">I", offset)
            values += new_value
        elif value_type == "Undefined":
            length = len(raw_value)
            if length > 4:
                offset = (TIFF_HEADER_LENGTH + ifd_offset +
                          entries_length + len(values))
                value_str = struct.pack(">I", offset)
                values += raw_value
            else:
                value_str = raw_value + b"\x00" * (4 - length)

        length_str = struct.pack(">I", length)
        entries += key_str + type_str + length_str + value_str
    return (entry_header + entries, values)
