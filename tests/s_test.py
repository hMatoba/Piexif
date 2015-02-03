import copy
import glob
import io
import os
import struct
import sys
import unittest

from PIL import Image
import piexif
from piexif import _common
from piexif._exif import TAGS

ImageIFD = piexif.ImageIFD
ExifIFD = piexif.ExifIFD
GPSIFD = piexif.GPSIFD

print("piexif version: {0}".format(piexif.VERSION))


INPUT_FILE1 = os.path.join("tests", "images", "01.jpg")
INPUT_FILE2 = os.path.join("tests", "images", "02.jpg")
INPUT_FILE_LE1 = os.path.join("tests", "images", "L01.jpg")
NOEXIF_FILE = os.path.join("tests", "images", "noexif.jpg")
# JPEG without APP0 and APP1 segments
NOAPP01_FILE = os.path.join("tests", "images", "noapp01.jpg")
INPUT_FILE_TIF = os.path.join("tests", "images", "01.tif")


with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()
with open(INPUT_FILE2, "rb") as f:
    I2 = f.read()


ZEROTH_DICT = {ImageIFD.Software: b"PIL", # ascii
               ImageIFD.Make: b"Make", # ascii
               ImageIFD.Model: b"XXX-XXX", # ascii
               ImageIFD.ResolutionUnit: 65535, # short
               ImageIFD.BitsPerSample: (24, 24, 24), # short * 3
               ImageIFD.XResolution: (4294967295, 1), # rational
               ImageIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1)),  # srational
               }


EXIF_DICT = {ExifIFD.DateTimeOriginal: b"2099:09:29 10:10:10", # ascii
             ExifIFD.LensMake: b"LensMake", # ascii
             ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa",  # undefined
             ExifIFD.Sharpness: 65535, # short
             ExifIFD.ISOSpeed: 4294967295, # long
             ExifIFD.ExposureTime: (4294967295, 1), # rational
             ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
             ExifIFD.ExposureBiasValue: (2147483647, -2147483648), # srational
             }


GPS_DICT = {GPSIFD.GPSVersionID: (0, 0, 0, 1), # byte
            GPSIFD.GPSAltitudeRef: 1, # byte
            GPSIFD.GPSDateStamp: b"1999:99:99 99:99:99", # ascii
            GPSIFD.GPSDifferential: 65535, # short
            GPSIFD.GPSLatitude: (4294967295, 1), # rational
            }


FIRST_DICT = {ImageIFD.Software: b"PIL", # ascii
              ImageIFD.Make: b"Make", # ascii
              ImageIFD.Model: b"XXX-XXX", # ascii
              ImageIFD.BitsPerSample: (24, 24, 24), # short * 3
              ImageIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1)),  # srational
              }


INTEROP_DICT = {piexif.InteropIFD.InteroperabilityIndex: b"R98"}


def load_exif_by_PIL(f):
    i = Image.open(f)
    e = i._getexif()
    i.close()
    return e


def pack_byte(*args):
    return struct.pack("B" * len(args), *args)


class ExifTests(unittest.TestCase):
    def test_merge_segments(self):
        # Remove APP0, when both APP0 and APP1 exists.
        with open(INPUT_FILE1, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments)
        segments = _common.split_into_segments(new_data)
        self.assertFalse([1][0:2] == b"\xff\xe0"
                        and segments[2][0:2] == b"\xff\xe1")
        self.assertEqual(segments[1][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        without_app0 = o.getvalue()
        Image.open(o).close()

        exif = _common.get_app1(segments)

        # Remove APP1, when second 'merged_segments' arguments is None
        # and no APP0.
        segments = _common.split_into_segments(without_app0)
        new_data = _common.merge_segments(segments, None)
        segments = _common.split_into_segments(new_data)
        self.assertNotEqual(segments[1][0:2], b"\xff\xe0")
        self.assertNotEqual(segments[1][0:2], b"\xff\xe1")
        self.assertNotEqual(segments[2][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

        # Insert exif to jpeg that has APP0 and APP1.
        o = io.BytesIO()
        i = Image.new("RGBA", (8, 8))
        i.save(o, format="jpeg", exif=exif)
        o.seek(0)
        segments = _common.split_into_segments(o.getvalue())
        new_data = _common.merge_segments(segments, exif)
        segments = _common.split_into_segments(new_data)
        self.assertFalse(segments[1][0:2] == b"\xff\xe0"
                         and segments[2][0:2] == b"\xff\xe1")
        self.assertEqual(segments[1], exif)
        o = io.BytesIO(new_data)
        Image.open(o).close()

        # Insert exif to jpeg that doesn't have APP0 and APP1.
        with open(NOAPP01_FILE, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments, exif)
        segments = _common.split_into_segments(new_data)
        self.assertEqual(segments[1][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

        # Remove APP1, when second 'merged_segments' arguments is None
        # and APP1 exists.
        with open(INPUT_FILE1, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments, None)
        segments = _common.split_into_segments(new_data)
        self.assertNotEqual(segments[1][0:2], b"\xff\xe1")
        self.assertNotEqual(segments[2][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

    def test_no_exif_load(self):
        exif_dict = piexif.load(NOEXIF_FILE)
        none_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "Interop":{},
                     "1st":{},
                     "thumbnail":None}
        self.assertEqual(exif_dict, none_dict)

    def test_no_exif_dump(self):
        o = io.BytesIO()
        exif_bytes = piexif.dump({})
        i = Image.new("RGBA", (8, 8))
        i.save(o, format="jpeg", exif=exif_bytes)
        o.seek(0)
        exif_dict2 = load_exif_by_PIL(o)
        self.assertDictEqual({},  exif_dict2)

    def test_transplant(self):
        piexif.transplant(INPUT_FILE1, INPUT_FILE2, "transplant.jpg")
        i = Image.open("transplant.jpg")
        i.close()
        exif_src = piexif.load(INPUT_FILE1)
        img_src = piexif.load(INPUT_FILE2)
        generated = piexif.load("transplant.jpg")
        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)

        piexif.transplant(INPUT_FILE1, "transplant.jpg")
        self.assertEqual(piexif.load(INPUT_FILE1),
                         piexif.load("transplant.jpg"))

        with  self.assertRaises(ValueError):
            piexif.transplant(NOEXIF_FILE, INPUT_FILE2, "foo.jpg")

    def test_transplant_m(self):
        """'transplant' on memory.
        """
        o = io.BytesIO()
        piexif.transplant(I1, I2, o)
        self.assertEqual(piexif.load(I1), piexif.load(o.getvalue()))
        Image.open(o).close()

    def test_remove(self):
        piexif.remove(INPUT_FILE1, "remove.jpg")
        exif_dict = piexif.load("remove.jpg")
        none_dict = {"0th":{},
                "Exif":{},
                "GPS":{},
                "Interop":{},
                "1st":{},
                "thumbnail":None}
        self.assertEqual(exif_dict, none_dict)

    def test_remove_m(self):
        """'remove' on memory.
        """
        o = io.BytesIO()
        with  self.assertRaises(ValueError):
            piexif.remove(I1)
        piexif.remove(I1, o)
        exif_dict = piexif.load(o.getvalue())
        none_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "Interop":{},
                     "1st":{},
                     "thumbnail":None}
        self.assertEqual(exif_dict, none_dict)
        Image.open(o).close()

    def test_load(self):
        exif = piexif.load(INPUT_FILE1)
        zeroth_dict = exif["0th"]
        exif_dict = exif["Exif"]
        gps_dict = exif["GPS"]
        e = load_exif_by_PIL(INPUT_FILE1)
        if 34853 in zeroth_dict:
            zeroth_dict.pop(34853)
        if 34853 in e:
            gps = e.pop(34853)
        for key in sorted(zeroth_dict):
            if key in e:
                if (isinstance(zeroth_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(zeroth_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(zeroth_dict[key], e[key])
                else:
                    self.assertEqual(zeroth_dict[key], e[key])
        for key in sorted(exif_dict):
            if key in e:
                if (isinstance(exif_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(exif_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(exif_dict[key], e[key])
                else:
                    self.assertEqual(exif_dict[key], e[key])
        for key in sorted(gps_dict):
            if key in gps:
                if (isinstance(gps_dict[key], tuple) and
                    (type(gps_dict[key]) != type(gps[key]))):
                    self.assertEqual(pack_byte(*gps_dict[key]), gps[key])
                elif (isinstance(gps_dict[key], int) and
                      (type(gps_dict[key]) != type(gps[key]))):
                    self.assertEqual(struct.pack("B", gps_dict[key]), gps[key])
                elif ((isinstance(gps_dict[key], bytes)) and
                      (isinstance(gps[key], str))):
                    try:
                        self.assertEqual(gps_dict[key].decode(), gps[key])
                    except:
                        self.assertEqual(gps_dict[key], gps[key])
                else:
                    self.assertEqual(gps_dict[key], gps[key])

    def test_load_m(self):
        """'load' on memory.
        """
        exif = piexif.load(I1)
        zeroth_dict = exif["0th"]
        exif_dict = exif["Exif"]
        gps_dict = exif["GPS"]
        e = load_exif_by_PIL(INPUT_FILE1)
        if 34853 in zeroth_dict:
            zeroth_dict.pop(34853)
        if 34853 in e:
            gps = e.pop(34853)
        for key in sorted(zeroth_dict):
            if key in e:
                if (isinstance(zeroth_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(zeroth_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(zeroth_dict[key], e[key])
                else:
                    self.assertEqual(zeroth_dict[key], e[key])
        for key in sorted(exif_dict):
            if key in e:
                if (isinstance(exif_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(exif_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(exif_dict[key], e[key])
                else:
                    self.assertEqual(exif_dict[key], e[key])
        for key in sorted(gps_dict):
            if key in gps:
                if (isinstance(gps_dict[key], tuple) and
                    (type(gps_dict[key]) != type(gps[key]))):
                    self.assertEqual(pack_byte(*gps_dict[key]), gps[key])
                elif (isinstance(gps_dict[key], int) and
                      (type(gps_dict[key]) != type(gps[key]))):
                    self.assertEqual(struct.pack("B", gps_dict[key]), gps[key])
                elif ((isinstance(gps_dict[key], bytes)) and
                      (isinstance(gps[key], str))):
                    try:
                        self.assertEqual(gps_dict[key].decode(), gps[key])
                    except:
                        self.assertEqual(gps_dict[key], gps[key])
                else:
                    self.assertEqual(gps_dict[key], gps[key])

    def test_load_le(self):
        """load test of little endian exif
        """
        exif = piexif.load(INPUT_FILE_LE1)
        zeroth_dict, exif_dict = exif["0th"], exif["Exif"]
        exif_dict.pop(41728) # value type is UNDEFINED but PIL returns int
        e = load_exif_by_PIL(INPUT_FILE_LE1)
        if 34853 in zeroth_dict:
            zeroth_dict.pop(34853)
        if 34853 in e:
            gps = e.pop(34853)
        for key in sorted(zeroth_dict):
            if key in e:
                if (isinstance(zeroth_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(zeroth_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(zeroth_dict[key], e[key])
                else:
                    self.assertEqual(zeroth_dict[key], e[key])
        for key in sorted(exif_dict):
            if key in e:
                if (isinstance(exif_dict[key], bytes) and
                    isinstance(e[key], str)):
                    try:
                        self.assertEqual(exif_dict[key].decode(), e[key])
                    except:
                        self.assertEqual(exif_dict[key], e[key])
                else:
                    self.assertEqual(exif_dict[key], e[key])

    def test_dump(self):
        exif_dict = {"0th":ZEROTH_DICT, "Exif":EXIF_DICT, "GPS":GPS_DICT}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGBA", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = load_exif_by_PIL(o)

    def test_insert(self):
        exif_dict = {"0th":ZEROTH_DICT, "Exif":EXIF_DICT, "GPS":GPS_DICT}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, INPUT_FILE1, "insert.jpg")
        exif = load_exif_by_PIL("insert.jpg")

        piexif.insert(exif_bytes, NOEXIF_FILE, "insert.jpg")

        with self.assertRaises(ValueError):
            piexif.insert(b"dummy", io.BytesIO())

        piexif.insert(exif_bytes, "insert.jpg")

    def test_insert_m(self):
        """'insert' on memory.
        """
        exif_dict = {"0th":ZEROTH_DICT, "Exif":EXIF_DICT, "GPS":GPS_DICT}
        exif_bytes = piexif.dump(exif_dict)
        o = io.BytesIO()
        piexif.insert(exif_bytes, I1, o)
        self.assertEqual(o.getvalue()[0:2], b"\xff\xd8")
        exif = load_exif_by_PIL(o)

    def test_dump_and_load(self):
        exif_dict = {"0th":ZEROTH_DICT, "Exif":EXIF_DICT, "GPS":GPS_DICT}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGBA", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = piexif.load(o.getvalue())
        zeroth_ifd, exif_ifd, gps_ifd = exif["0th"], exif["Exif"], exif["GPS"]
        zeroth_ifd.pop(ImageIFD.ExifTag) # pointer to exif IFD
        zeroth_ifd.pop(ImageIFD.GPSTag) # pointer to GPS IFD
        self.assertDictEqual(ZEROTH_DICT, zeroth_ifd)
        self.assertDictEqual(EXIF_DICT, exif_ifd)
        self.assertDictEqual(GPS_DICT, gps_ifd)

    def test_load_tif(self):
        exif = piexif.load(INPUT_FILE_TIF)
        zeroth_ifd = exif["0th"]
        exif_bytes = piexif.dump({"0th":zeroth_ifd})

        im = Image.new("RGBA", (8, 8))
        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif2 = piexif.load(o.getvalue())
        zeroth_ifd2 = exif2["0th"]
        self.assertDictEqual(zeroth_ifd, zeroth_ifd2)

    def test_dump_and_load_2(self):
        thumbnail_io = io.BytesIO()
        thumb = Image.open(INPUT_FILE2)
        thumb.thumbnail((40, 40))
        thumb.save(thumbnail_io, "JPEG")
        thumb.close()
        thumb.seek(0)
        thumb_data = thumbnail_io.getvalue()
        print(len(thumb_data))
        exif_dict = {"0th":ZEROTH_DICT,
                     "Exif":EXIF_DICT,
                     "GPS":GPS_DICT,
                     "Interop":INTEROP_DICT,
                     "1st":FIRST_DICT,
                     "thumbnail":thumb_data}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGBA", (80, 80))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = piexif.load(o.getvalue())
        exif["0th"].pop(ImageIFD.ExifTag) # pointer to exif IFD
        exif["0th"].pop(ImageIFD.GPSTag) # pointer to GPS IFD
        exif["0th"].pop(ImageIFD.InteroperabilityPointer)
        self.assertDictEqual(ZEROTH_DICT, exif["0th"])
        self.assertDictEqual(EXIF_DICT, exif["Exif"])
        self.assertDictEqual(GPS_DICT, exif["GPS"])
        self.assertDictEqual(INTEROP_DICT, exif["Interop"])
        exif["1st"].pop(513) # pointer to exif IFD
        exif["1st"].pop(514) # pointer to GPS IFD
        self.assertDictEqual(FIRST_DICT, exif["1st"])
        print(len(exif["thumbnail"]))
        Image.open(io.BytesIO(exif["thumbnail"])).close()

    def test_roundtrip_files(self):
        files = glob.glob(os.path.join("tests", "images", "r_*.jpg"))
        for input_file in files:
            exif = piexif.load(input_file)
            exif_bytes = piexif.dump(exif)
            o = io.BytesIO()
            piexif.insert(exif_bytes, input_file, o)
            e = piexif.load(o.getvalue())
            if "thumbnail" in e:
                t = e.pop("thumbnail")
                thumbnail = exif.pop("thumbnail")
                if not (b"\xe0" <= thumbnail[3:4] <= b"\xef"):
                    self.assertEqual(t, thumbnail)
                else:
                    print("Given JPEG doesn't follow exif thumbnail standard. "
                          "APPn segments in thumbnail should be removed, "
                          "whereas thumbnail JPEG has it. \n: " +
                          input_file)
            for ifd_name in e:
                if ifd_name == "0th":
                    if ImageIFD.ExifTag in exif["0th"]:
                        exif["0th"].pop(ImageIFD.ExifTag)
                        e["0th"].pop(ImageIFD.ExifTag)
                    if ImageIFD.GPSTag in exif["0th"]:
                        exif["0th"].pop(ImageIFD.GPSTag)
                        e["0th"].pop(ImageIFD.GPSTag)
                    if ImageIFD.InteroperabilityPointer in exif["0th"]:
                        exif["0th"].pop(ImageIFD.InteroperabilityPointer)
                        e["0th"].pop(ImageIFD.InteroperabilityPointer)
                elif ifd_name == "1st":
                    exif["1st"].pop(513)
                    e["1st"].pop(513)
                    exif["1st"].pop(514)
                    e["1st"].pop(514)
                for key in exif[ifd_name]:
                    self.assertEqual(exif[ifd_name][key], e[ifd_name][key])


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ExifTests))
    return suite


if __name__ == '__main__':
    unittest.main()