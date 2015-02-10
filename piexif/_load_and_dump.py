import copy
import io
import struct
import sys

from ._common import *
from ._exif import *


if sys.version_info[0] == 2:
    NUMBER_TYPE = (int, long)
else:
    NUMBER_TYPE = int


TYPES = {"Byte": 1,
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

BYTE_LENGTH = 1
SHORT_LENGTH = 2
LONG_LENGTH = 4


class ExifReader(object):
    def __init__(self, data):
        if data[0:2] == b"\xff\xd8":  # JPEG
            segments = split_into_segments(data)
            app1 = get_app1(segments)
            if app1:
                self.tiftag = app1[10:]
            else:
                self.tiftag = None
        elif data[0:2] in (b"\x49\x49", b"\x4d\x4d"):  # TIFF
            self.tiftag = data
        elif data[0:4] == b"Exif":  # Exif
            self.tiftag = data[6:]
        elif data[-4:].lower() in (".jpg", "jpeg", ".jpe", ".tif", "tiff"):
            with open(data, 'rb') as f:
                data = f.read()
            if data[0:2] == b"\xff\xd8":  # JPEG
                segments = split_into_segments(data)
                app1 = get_app1(segments)
                if app1:
                    self.tiftag = app1[10:]
                else:
                    self.tiftag = None
            elif data[0:2] in (b"\x49\x49", b"\x4d4d"):  # TIFF
                self.tiftag = data
            else:
                raise ValueError("Given file is neither JPEG nor TIFF.")
        else:
            raise ValueError("Given file is neither JPEG nor TIFF.")

    def get_ifd_dict(self, pointer, ifd_name, read_unknown=False):
        ifd_dict = {}
        tag_count = struct.unpack(self.endian_mark + "H",
                                  self.tiftag[pointer: pointer+2])[0]
        offset = pointer + 2
        if ifd_name in ["0th", "1st"]:
            t = "Image"
        else:
            t = ifd_name
        p_and_value = []
        for x in range(tag_count):
            pointer = offset + 12 * x
            tag = struct.unpack(self.endian_mark + "H",
                       self.tiftag[pointer: pointer+2])[0]
            value_type = struct.unpack(self.endian_mark + "H",
                         self.tiftag[pointer + 2: pointer + 4])[0]
            value_num = struct.unpack(self.endian_mark + "L",
                                      self.tiftag[pointer + 4: pointer + 8]
                                      )[0]
            value = self.tiftag[pointer+8: pointer+12]
            p_and_value.append((pointer, value_type, value_num, value))
            v_set = (value_type, value_num, value)
            if tag in TAGS[t]:
                ifd_dict[tag] = self.convert_value(v_set)
            elif read_unknown:
                ifd_dict[tag] = (v_set[0], v_set[1], v_set[2], self.tiftag)
            #else:
            #    pass

        if ifd_name == "0th":
            pointer = offset + 12 * tag_count
            ifd_dict["first_ifd_pointer"] = self.tiftag[pointer:pointer + 4]
        return ifd_dict

    def convert_value(self, val):
        data = None
        t = val[0]
        length = val[1]
        value = val[2]

        if t == 1: # BYTE
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack("B" * length,
                                     self.tiftag[pointer: pointer + length])
            else:
                data = struct.unpack("B" * length, value[0:length])
        elif t == 2: # ASCII
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = self.tiftag[pointer: pointer+length - 1]
            else:
                data = value[0: length - 1]
        elif t == 3: # SHORT
            if length > 2:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "H" * length,
                                     self.tiftag[pointer: pointer+length*2])
            else:
                data = struct.unpack(self.endian_mark + "H" * length,
                                     value[0:length * 2])
        elif t == 4: # LONG
            if length > 1:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "L" * length,
                                     self.tiftag[pointer: pointer+length*4])
            else:
                data = struct.unpack(self.endian_mark + "L" * length,
                                     value)
        elif t == 5: # RATIONAL
            pointer = struct.unpack(self.endian_mark + "L", value)[0]
            if length > 1:
                data = tuple(
                    (struct.unpack(self.endian_mark + "L",
                                   self.tiftag[pointer + x * 8:
                                       pointer + 4 + x * 8])[0],
                     struct.unpack(self.endian_mark + "L",
                                   self.tiftag[pointer + 4 + x * 8:
                                       pointer + 8 + x * 8])[0])
                    for x in range(length)
                )
            else:
                data = (struct.unpack(self.endian_mark + "L",
                                      self.tiftag[pointer: pointer + 4])[0],
                        struct.unpack(self.endian_mark + "L",
                                      self.tiftag[pointer + 4: pointer + 8]
                                      )[0])
        elif t == 7: # UNDEFINED BYTES
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = self.tiftag[pointer: pointer+length]
            else:
                data = value[0:length]
#        elif t == 9: # SLONG
#            if length > 1:
#                pointer = struct.unpack(self.endian_mark + "L", value)[0]
#                data = struct.unpack(self.endian_mark + "l" * length,
#                                     self.exif_str[pointer: pointer+length*4])
#            else:
#                data = struct.unpack(self.endian_mark + "l" * length,
#                                     value)
        elif t == 10: # SRATIONAL
            pointer = struct.unpack(self.endian_mark + "L", value)[0]
            if length > 1:
                data = tuple(
                  (struct.unpack(self.endian_mark + "l",
                   self.tiftag[pointer + x * 8: pointer + 4 + x * 8])[0],
                   struct.unpack(self.endian_mark + "l",
                   self.tiftag[pointer + 4 + x * 8: pointer + 8 + x * 8])[0])
                  for x in range(length)
                )
            else:
                data = (struct.unpack(self.endian_mark + "l",
                                      self.tiftag[pointer: pointer + 4])[0],
                        struct.unpack(self.endian_mark + "l",
                                      self.tiftag[pointer + 4: pointer + 8]
                                      )[0])
        else:
            raise ValueError("Exif might be wrong. Got incorrect value " +
                             "type to decode.")

        if isinstance(data, tuple) and (len(data) == 1):
            return data[0]
        else:
            return data


def load(input_data):
    r"""
    py:function:: piexif.load(filename)

    Return exif data as dict. Keys(IFD name), be contained, are "0th", "Exif", "GPS", "Interop", "1st", and "thumbnail". Without "thumbnail", the value is dict(tag name/tag value). "thumbnail" value is JPEG as bytes.

    :param str filename: JPEG or TIFF
    :return: Exif data({"0th":dict, "Exif":dict, "GPS":dict, "Interop":dict, "1st":dict, "thumbnail":bytes})
    :rtype: dict
    """
    exif_dict = {"0th":{},
                 "Exif":{},
                 "GPS":{},
                 "Interop":{},
                 "1st":{},
                 "thumbnail":None}
    exifReader = ExifReader(input_data)
    if exifReader.tiftag is None:
        return exif_dict

    if exifReader.tiftag[0:2] == LITTLE_ENDIAN:
        exifReader.endian_mark = "<"
    else:
        exifReader.endian_mark = ">"

    pointer = struct.unpack(exifReader.endian_mark + "L",
                            exifReader.tiftag[4:8])[0]
    exif_dict["0th"] = exifReader.get_ifd_dict(pointer, "0th")
    first_ifd_pointer = exif_dict["0th"].pop("first_ifd_pointer")
    if 34665 in exif_dict["0th"]:
        pointer = exif_dict["0th"][34665]
        exif_dict["Exif"] = exifReader.get_ifd_dict(pointer, "Exif")
    if 34853 in exif_dict["0th"]:
        pointer = exif_dict["0th"][34853]
        exif_dict["GPS"] = exifReader.get_ifd_dict(pointer, "GPS")
    if 40965 in exif_dict["Exif"]:
        pointer = exif_dict["Exif"][40965]
        exif_dict["Interop"] = exifReader.get_ifd_dict(pointer, "Interop")
    if first_ifd_pointer != b"\x00\x00\x00\x00":
        pointer = struct.unpack(exifReader.endian_mark + "L",
                                first_ifd_pointer)[0]
        exif_dict["1st"] = exifReader.get_ifd_dict(pointer, "1st")
        if (513 in exif_dict["1st"]) and (514 in exif_dict["1st"]):
            end = exif_dict["1st"][513]+exif_dict["1st"][514]
            thumb = exifReader.tiftag[exif_dict["1st"][513]:end]
            exif_dict["thumbnail"] = thumb
    return exif_dict


def dump(exif_dict_original):
    """
    py:function:: piexif.load(data)

    Return exif as bytes.

    :param dict exif: Exif data({"0th":dict, "Exif":dict, "GPS":dict, "Interop":dict, "1st":dict, "thumbnail":bytes})
    :return: Exif
    :rtype: bytes
    """
    exif_dict = copy.deepcopy(exif_dict_original)
    header = b"Exif\x00\x00\x4d\x4d\x00\x2a\x00\x00\x00\x08"
    exif_is = False
    gps_is = False
    interop_is = False
    first_is = False

    if "0th" in exif_dict:
        zeroth_ifd = exif_dict["0th"]
    else:
        zeroth_ifd = {}
    if (("Exif" in exif_dict) and len(exif_dict["Exif"]) or
          ("Interop" in exif_dict) and len(exif_dict["Interop"]) ):
        zeroth_ifd[34665] = 1
        exif_is = True
        exif_ifd = exif_dict["Exif"]
        if ("Interop" in exif_dict) and len(exif_dict["Interop"]):
            exif_ifd[40965] = 1
            interop_is = True
            interop_ifd = exif_dict["Interop"]
    if ("GPS" in exif_dict) and len(exif_dict["GPS"]):
        zeroth_ifd[34853] = 1
        gps_is = True
        gps_ifd = exif_dict["GPS"]
    if (("1st" in exif_dict) and
            ("thumbnail" in exif_dict) and
            (exif_dict["thumbnail"] is not None)):
        first_is = True
        exif_dict["1st"][513] = 1
        exif_dict["1st"][514] = 1
        first_ifd = exif_dict["1st"]

    zeroth_set = dict_to_bytes(zeroth_ifd, "0th", 0)
    zeroth_length = (len(zeroth_set[0]) + exif_is * 12 + gps_is * 12 + 4 + 
                     len(zeroth_set[1]))

    if exif_is:
        exif_set = dict_to_bytes(exif_ifd, "Exif", zeroth_length)
        exif_length = len(exif_set[0]) + interop_is * 12 + len(exif_set[1])
        #exif_bytes = b"".join(exif_set)
        #exif_length = len(exif_bytes)
    else:
        exif_bytes = b""
        exif_length = 0
    if gps_is:
        gps_set = dict_to_bytes(gps_ifd, "GPS", zeroth_length + exif_length)
        gps_bytes = b"".join(gps_set)
        gps_length = len(gps_bytes)
    else:
        gps_bytes = b""
        gps_length = 0
    if interop_is:
        offset = zeroth_length + exif_length + gps_length
        interop_set = dict_to_bytes(interop_ifd, "Interop", offset)
        interop_bytes = b"".join(interop_set)
        interop_length = len(interop_bytes)
    else:
        interop_bytes = b""
        interop_length = 0
    if first_is:
        offset = zeroth_length + exif_length + gps_length + interop_length
        first_set = dict_to_bytes(first_ifd, "1st", offset)
        thumbnail = get_thumbnail(exif_dict["thumbnail"])
        if len(thumbnail) > 64000:
            raise ValueError("Given thumbnail is too large. max 64kB")
    else:
        first_bytes = b""

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
    if interop_is:
        pointer_value = (TIFF_HEADER_LENGTH +
                         zeroth_length + exif_length + gps_length)
        pointer_str = struct.pack(">I", pointer_value)
        key = 40965
        key_str = struct.pack(">H", key)
        type_str = struct.pack(">H", TYPES["Long"])
        length_str = struct.pack(">I", 1)
        interop_pointer = key_str + type_str + length_str + pointer_str
    else:
        interop_pointer = b""
    if first_is:
        pointer_value = (TIFF_HEADER_LENGTH + zeroth_length +
                         exif_length + gps_length + interop_length)
        first_ifd_pointer = struct.pack(">L", pointer_value)
        thumbnail_pointer = (pointer_value + len(first_set[0]) + 24 +
                             4 + len(first_set[1]))
        thumbnail_p_bytes = (b"\x02\x01\x00\x04\x00\x00\x00\x01" +
                             struct.pack(">L", thumbnail_pointer))
        thumbnail_length_bytes = (b"\x02\x02\x00\x04\x00\x00\x00\x01" +
                                  struct.pack(">L", len(thumbnail)))
        first_bytes = (first_set[0] + thumbnail_p_bytes +
                       thumbnail_length_bytes + b"\x00\x00\x00\x00" +
                       first_set[1] + thumbnail)
    else:
        first_ifd_pointer = b"\x00\x00\x00\x00"

    zeroth_bytes = (zeroth_set[0] + exif_pointer + gps_pointer +
                    first_ifd_pointer + zeroth_set[1])
    if exif_is:
        exif_bytes = exif_set[0] + interop_pointer + exif_set[1]

    return (header + zeroth_bytes + exif_bytes + gps_bytes +
            interop_bytes + first_bytes)


def get_thumbnail(jpeg):
    segments = split_into_segments(jpeg)
    while (b"\xff\xe0" <= segments[1][0:2] <= b"\xff\xef"):
        segments.pop(1)
    thumbnail = b"".join(segments)
    return thumbnail


def pack_byte(*args):
    return struct.pack("B" * len(args), *args)


def pack_short(*args):
    return struct.pack(">" + "H" * len(args), *args)


def pack_long(*args):
    return struct.pack(">" + "L" * len(args), *args)


#def pack_slong(*args):
#    return struct.pack(">" + "l" * len(args), *args)


def value_to_bytes(raw_value, value_type, offset):
    four_bytes_over = b""
    value_str = b""

    if value_type == "Byte":
        length = len(raw_value)
        if length <= 4:
            value_str = (pack_byte(*raw_value) +
                            b"\x00" * (4 - length))
        else:
            value_str = struct.pack(">I", offset)
            four_bytes_over = pack_byte(*raw_value)
    elif value_type == "Short":
        length = len(raw_value)
        if length <= 2:
            value_str = (pack_short(*raw_value) +
                            b"\x00\x00" * (2 - length))
        else:
            value_str = struct.pack(">I", offset)
            four_bytes_over = pack_short(*raw_value)
    elif value_type == "Long":
        length = len(raw_value)
        if length <= 1:
            value_str = pack_long(*raw_value)
        else:
            value_str = struct.pack(">I", offset)
            four_bytes_over = pack_long(*raw_value)
#        elif value_type == "SLong":
#            length = len(raw_value)
#            if length <= 1:
#                value_str = pack_long(*raw_value)
#            else:
#                value_str = struct.pack(">I", offset)
#                four_bytes_over = pack_slong(*raw_value)
    elif value_type == "Ascii":
        try:
            new_value = raw_value.encode("latin1") + b"\x00"
        except:
            new_value = raw_value + b"\x00"
        length = len(new_value)
        if length > 4:
            value_str = struct.pack(">I", offset)
            four_bytes_over = new_value
        else:
            value_str = new_value + b"\x00" * (4 - length)
    elif value_type == "Rational":
        if isinstance(raw_value[0], NUMBER_TYPE):
            length = 1
            num, den = raw_value
            new_value = struct.pack(">L", num) + struct.pack(">L", den)
        elif isinstance(raw_value[0], tuple):
            length = len(raw_value)
            new_value = b""
            for n, val in enumerate(raw_value):
                num, den = val
                new_value += (struct.pack(">L", num) +
                                struct.pack(">L", den))
        value_str = struct.pack(">I", offset)
        four_bytes_over = new_value
    elif value_type == "SRational":
        if isinstance(raw_value[0], NUMBER_TYPE):
            length = 1
            num, den = raw_value
            new_value = struct.pack(">l", num) + struct.pack(">l", den)
        elif isinstance(raw_value[0], tuple):
            length = len(raw_value)
            new_value = b""
            for n, val in enumerate(raw_value):
                num, den = val
                new_value += (struct.pack(">l", num) +
                                struct.pack(">l", den))
        value_str = struct.pack(">I", offset)
        four_bytes_over = new_value
    elif value_type == "Undefined":
        length = len(raw_value)
        if length > 4:
            value_str = struct.pack(">I", offset)
            four_bytes_over = raw_value
        else:
            value_str = raw_value + b"\x00" * (4 - length)

    length_str = struct.pack(">I", length)
    return length_str, value_str, four_bytes_over

def dict_to_bytes(ifd_dict, ifd, ifd_offset):
    tag_count = len(ifd_dict)
    entry_header = struct.pack(">H", tag_count)
    if ifd in ("0th", "1st"):
        entries_length = 2 + tag_count * 12 + 4
    else:
        entries_length = 2 + tag_count * 12
    entries = b""
    values = b""

    for n, key in enumerate(sorted(ifd_dict)):
        if (ifd == "0th") and (key in (34665, 34853)):
            continue
        elif (ifd == "Exif") and (key == 40965):
            continue
        elif (ifd == "1st") and (key in (513, 514)):
            continue

        raw_value = ifd_dict[key]
        key_str = struct.pack(">H", key)
        value_type = TAGS[ifd][key]["type"]
        type_str = struct.pack(">H", TYPES[value_type])
        four_bytes_over = b""

        if isinstance(raw_value, NUMBER_TYPE):
            raw_value = (raw_value,)
        offset = TIFF_HEADER_LENGTH + entries_length + ifd_offset + len(values)

        length_str, value_str, four_bytes_over = value_to_bytes(raw_value,
                                                                value_type,
                                                                offset)
        entries += key_str + type_str + length_str + value_str
        values += four_bytes_over
    return (entry_header + entries, values)
