import struct
import sys

from . import _webp
from ._common import get_exif_seg, read_exif_from_file, split_into_segments
from ._exceptions import InvalidImageDataError
from ._exif import ExifIFD, ImageIFD, TAGS, TYPES


LITTLE_ENDIAN = b"\x49\x49"


def load(input_data, key_is_name=False):
    """
    py:function:: piexif.load(input_data, key_is_name=False)

    Return exif data as dict. Keys(IFD name), be contained, are "0th", "Exif", "GPS", "Interop",
    "1st", and "thumbnail". Without "thumbnail", the value is dict(tag name/tag value).
    "thumbnail" value is JPEG as bytes.

    :type input_data: str or bytes
    :type key_is_name: bool
    :return: Exif data({"0th":dict, "Exif":dict, "GPS":dict, "Interop":dict, "1st":dict, "thumbnail":bytes})
    :rtype: dict
    """
    exif_dict, _ = _load_and_parse(input_data, key_is_name)
    return exif_dict


def safe_load(input_data, key_is_name=False):
    """
    py:function:: piexif.safe_load(input_data, key_is_name=False)

    Returns tuple with exif data as dict and list of errors.
    Keys(IFD name) of dictionary, be contained, are "0th", "Exif", "GPS", "Interop",
    "1st", and "thumbnail". Without "thumbnail", the value is dict(tag name/tag value).
    "thumbnail" value is JPEG as bytes.

    :type input_data: str or bytes
    :type key_is_name: bool
    :rtype: tuple(dict, list)
    """
    return _load_and_parse(input_data, key_is_name, raise_errors=False)


def _load_and_parse(input_data, key_is_name=False, raise_errors=True):
    exif_dict = {"0th":{},
                 "Exif":{},
                 "GPS":{},
                 "Interop":{},
                 "1st":{},
                 "thumbnail":None}
    exifReader = _ExifReader(input_data, raise_errors)
    if exifReader.tiftag is None:
        return exif_dict, [(None, None, 'EXIF has not found')]

    pointer = struct.unpack(exifReader.endian_mark + "L",
                            exifReader.tiftag[4:8])[0]
    exif_dict["0th"], all_errors = exifReader.get_ifd_dict(pointer, "0th")
    first_ifd_pointer = exif_dict["0th"].pop("first_ifd_pointer")
    if ImageIFD.ExifTag in exif_dict["0th"]:
        pointer = exif_dict["0th"][ImageIFD.ExifTag]
        exif_dict["Exif"], errors = exifReader.get_ifd_dict(pointer, "Exif")
        all_errors += errors
    if ImageIFD.GPSTag in exif_dict["0th"]:
        pointer = exif_dict["0th"][ImageIFD.GPSTag]
        exif_dict["GPS"], errors = exifReader.get_ifd_dict(pointer, "GPS")
        all_errors += errors
    if ExifIFD.InteroperabilityTag in exif_dict["Exif"]:
        pointer = exif_dict["Exif"][ExifIFD.InteroperabilityTag]
        exif_dict["Interop"], errors = exifReader.get_ifd_dict(pointer, "Interop")
        all_errors += errors
    if first_ifd_pointer != b"\x00\x00\x00\x00":
        pointer = struct.unpack(exifReader.endian_mark + "L",
                                first_ifd_pointer)[0]
        exif_dict["1st"], errors = exifReader.get_ifd_dict(pointer, "1st")
        all_errors += errors
        if (ImageIFD.JPEGInterchangeFormat in exif_dict["1st"] and
                ImageIFD.JPEGInterchangeFormatLength in exif_dict["1st"]):
            end = (exif_dict["1st"][ImageIFD.JPEGInterchangeFormat] +
                   exif_dict["1st"][ImageIFD.JPEGInterchangeFormatLength])
            thumb = exifReader.tiftag[exif_dict["1st"][ImageIFD.JPEGInterchangeFormat]:end]
            exif_dict["thumbnail"] = thumb

    if key_is_name:
        exif_dict = _get_key_name_dict(exif_dict)
    return exif_dict, all_errors


class _ExifReader(object):
    def __init__(self, data, raise_errors=True):
        self.raise_errors = raise_errors
        # Prevents "UnicodeWarning: Unicode equal comparison failed" warnings on Python 2
        maybe_image = sys.version_info >= (3,0,0) or isinstance(data, str)

        if maybe_image and data[0:2] == b"\xff\xd8":  # JPEG
            segments = split_into_segments(data)
            app1 = get_exif_seg(segments)
            if app1:
                self.tiftag = app1[10:]
            else:
                self.tiftag = None
        elif maybe_image and data[0:2] in (b"\x49\x49", b"\x4d\x4d"):  # TIFF
            self.tiftag = data
        elif maybe_image and data[0:4] == b"RIFF" and data[8:12] == b"WEBP":
            self.tiftag = _webp.get_exif(data)
        elif maybe_image and data[0:4] == b"Exif":  # Exif
            self.tiftag = data[6:]
        else:
            with open(data, 'rb') as f:
                magic_number = f.read(2)
            if magic_number == b"\xff\xd8":  # JPEG
                app1 = read_exif_from_file(data)
                if app1:
                    self.tiftag = app1[10:]
                else:
                    self.tiftag = None
            elif magic_number in (b"\x49\x49", b"\x4d\x4d"):  # TIFF
                with open(data, 'rb') as f:
                    self.tiftag = f.read()
            else:
                with open(data, 'rb') as f:
                    header = f.read(12)
                if header[0:4] == b"RIFF"and header[8:12] == b"WEBP":
                    with open(data, 'rb') as f:
                        file_data = f.read()
                    self.tiftag = _webp.get_exif(file_data)
                else:
                    raise InvalidImageDataError("Given file is neither JPEG nor TIFF.")

        if self.tiftag and self.tiftag[0:2] == LITTLE_ENDIAN:
            self.endian_mark = "<"
        else:
            self.endian_mark = ">"

    def get_ifd_dict(self, pointer, ifd_name, read_unknown=False):
        ifd_dict = {}
        try:
            tag_count = struct.unpack(self.endian_mark + "H",
                                      self.tiftag[pointer: pointer + 2])[0]
        except struct.error:
            if self.raise_errors:
                raise
            return ifd_dict, [(ifd_name, None, 'Bad SubDirectory start.')]

        errors = []
        offset = pointer + 2
        if ifd_name in ["0th", "1st"]:
            t = "Image"
        else:
            t = ifd_name
        p_and_value = []
        for x in range(tag_count):
            pointer = offset + 12 * x
            tag = None
            try:
                tag = struct.unpack(self.endian_mark + "H",
                                    self.tiftag[pointer: pointer + 2])[0]
                value_type = struct.unpack(self.endian_mark + "H",
                                           self.tiftag[pointer + 2: pointer + 4])[0]
                value_num = struct.unpack(self.endian_mark + "L",
                                          self.tiftag[pointer + 4: pointer + 8]
                                          )[0]
                value = self.tiftag[pointer + 8: pointer + 12]
            except Exception as e:
                if self.raise_errors:
                    raise
                errors.append((ifd_name, tag, str(e)))
                continue

            p_and_value.append((pointer, value_type, value_num, value))
            v_set = (value_type, value_num, value, tag)
            try:
                if tag in TAGS[t]:
                    ifd_dict[tag] = self.convert_value(v_set)
                elif read_unknown:
                    ifd_dict[tag] = (v_set[0], v_set[1], v_set[2], self.tiftag)
            except Exception as e:
                if self.raise_errors:
                    raise
                errors.append((ifd_name, tag, str(e)))

        if ifd_name == "0th":
            pointer = offset + 12 * tag_count
            ifd_dict["first_ifd_pointer"] = self.tiftag[pointer:pointer + 4]
        return ifd_dict, errors

    def convert_value(self, val):
        data = None
        t = val[0]
        length = val[1]
        value = val[2]

        if t == TYPES.Byte: # BYTE
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack("B" * length,
                                     self.tiftag[pointer: pointer + length])
            else:
                data = struct.unpack("B" * length, value[0:length])
        elif t == TYPES.Ascii: # ASCII
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = self.tiftag[pointer: pointer+length - 1]
            else:
                data = value[0: length - 1]
        elif t == TYPES.Short: # SHORT
            if length > 2:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "H" * length,
                                     self.tiftag[pointer: pointer+length*2])
            else:
                data = struct.unpack(self.endian_mark + "H" * length,
                                     value[0:length * 2])
        elif t == TYPES.Long: # LONG
            if length > 1:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "L" * length,
                                     self.tiftag[pointer: pointer+length*4])
            else:
                data = struct.unpack(self.endian_mark + "L" * length,
                                     value)
        elif t == TYPES.Rational: # RATIONAL
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
        elif t == TYPES.SByte: # SIGNED BYTES
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack("b" * length,
                                     self.tiftag[pointer: pointer + length])
            else:
                data = struct.unpack("b" * length, value[0:length])
        elif t == TYPES.Undefined: # UNDEFINED BYTES
            if length > 4:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = self.tiftag[pointer: pointer+length]
            else:
                data = value[0:length]
        elif t == TYPES.SShort: # SIGNED SHORT
            if length > 2:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "h" * length,
                                     self.tiftag[pointer: pointer+length*2])
            else:
                data = struct.unpack(self.endian_mark + "h" * length,
                                     value[0:length * 2])
        elif t == TYPES.SLong: # SLONG
            if length > 1:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "l" * length,
                                     self.tiftag[pointer: pointer+length*4])
            else:
                data = struct.unpack(self.endian_mark + "l" * length,
                                     value)
        elif t == TYPES.SRational: # SRATIONAL
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
        elif t == TYPES.Float: # FLOAT
            if length > 1:
                pointer = struct.unpack(self.endian_mark + "L", value)[0]
                data = struct.unpack(self.endian_mark + "f" * length,
                                     self.tiftag[pointer: pointer+length*4])
            else:
                data = struct.unpack(self.endian_mark + "f" * length,
                                     value)
        elif t == TYPES.DFloat: # DOUBLE
            pointer = struct.unpack(self.endian_mark + "L", value)[0]
            data = struct.unpack(self.endian_mark + "d" * length,
                                    self.tiftag[pointer: pointer+length*8])
        else:
            raise ValueError("Exif might be wrong. Got incorrect value " +
                             "type to decode.\n" +
                             "tag: " + str(val[3]) + "\ntype: " + str(t))

        if isinstance(data, tuple) and (len(data) == 1):
            return data[0]
        else:
            return data


def _get_key_name_dict(exif_dict):
    new_dict = {
        ifd_name: {
            TAGS[ifd_name][n]["name"]: value
            for n, value in exif_dict[ifd_name].items()
        }
        for ifd_name in ("0th", "Exif", "1st", "GPS", "Interop")
    }
    new_dict["thumbnail"] = exif_dict["thumbnail"]
    return new_dict
