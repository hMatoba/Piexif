# -*- coding: utf-8 -*-

import copy
import glob
import io
import os
import struct
import sys
import time
import unittest

from PIL import Image
import piexif
from piexif import _common, ImageIFD, ExifIFD, GPSIFD, TAGS, InvalidImageDataError
from piexif import _webp
from piexif import helper


print("piexif version: {}".format(piexif.VERSION))


INPUT_FILE1 = os.path.join("tests", "images", "01.jpg")
INPUT_FILE2 = os.path.join("tests", "images", "02.jpg")
INPUT_FILE_PEN = os.path.join("tests", "images", "r_pen.jpg")
NOEXIF_FILE = os.path.join("tests", "images", "noexif.jpg")
# JPEG without APP0 and APP1 segments
NOAPP01_FILE = os.path.join("tests", "images", "noapp01.jpg")
INPUT_FILE_TIF = os.path.join("tests", "images", "01.tif")


with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()
with open(INPUT_FILE2, "rb") as f:
    I2 = f.read()


ZEROTH_IFD = {ImageIFD.Software: b"PIL", # ascii
               ImageIFD.Make: b"Make", # ascii
               ImageIFD.Model: b"XXX-XXX", # ascii
               ImageIFD.ResolutionUnit: 65535, # short
               ImageIFD.BitsPerSample: (24, 24, 24), # short * 3
               ImageIFD.XResolution: (4294967295, 1), # rational
               ImageIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1)), # srational
               ImageIFD.ZZZTestSlong1: -11,
               ImageIFD.ZZZTestSlong2: (-11, -11, -11, -11),
               }


EXIF_IFD = {ExifIFD.DateTimeOriginal: b"2099:09:29 10:10:10", # ascii
             ExifIFD.LensMake: b"LensMake", # ascii
             ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa",  # undefined
             ExifIFD.Sharpness: 65535, # short
             ExifIFD.ISOSpeed: 4294967295, # long
             ExifIFD.ExposureTime: (4294967295, 1), # rational
             ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
             ExifIFD.ExposureBiasValue: (2147483647, -2147483648), # srational
             }


GPS_IFD = {GPSIFD.GPSVersionID: (0, 0, 0, 1), # byte
            GPSIFD.GPSAltitudeRef: 1, # byte
            GPSIFD.GPSDateStamp: b"1999:99:99 99:99:99", # ascii
            GPSIFD.GPSDifferential: 65535, # short
            GPSIFD.GPSLatitude: (4294967295, 1), # rational
            }


FIRST_IFD = {ImageIFD.Software: b"PIL", # ascii
              ImageIFD.Make: b"Make", # ascii
              ImageIFD.Model: b"XXX-XXX", # ascii
              ImageIFD.BitsPerSample: (24, 24, 24), # short * 3
              ImageIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1)),  # srational
              }


INTEROP_IFD = {piexif.InteropIFD.InteroperabilityIndex: b"R98"}


def load_exif_by_PIL(f):
    i = Image.open(f)
    e = i._getexif()
    i.close()
    return e


def pack_byte(*args):
    return struct.pack("B" * len(args), *args)


class ExifTests(unittest.TestCase):
    """tests for main five functions."""

# load ------
    def test_no_exif_load(self):
        exif_dict = piexif.load(NOEXIF_FILE)
        none_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "Interop":{},
                     "1st":{},
                     "thumbnail":None}
        self.assertEqual(exif_dict, none_dict)

    def test_load(self):
        files = glob.glob(os.path.join("tests", "images", "r_*.jpg"))
        for input_file in files:
            exif = piexif.load(input_file)
            e = load_exif_by_PIL(input_file)
            print("********************\n" + input_file + "\n")
            self._compare_piexifDict_PILDict(exif, e, p=False)

    def test_load_m(self):
        """'load' on memory.
        """
        exif = piexif.load(I1)
        e = load_exif_by_PIL(INPUT_FILE1)
        print("********************\n\n" + INPUT_FILE1 + "\n")
        self._compare_piexifDict_PILDict(exif, e)

    def test_load_tif(self):
        exif = piexif.load(INPUT_FILE_TIF)
        zeroth_ifd = exif["0th"]
        exif_bytes = piexif.dump({"0th":zeroth_ifd})

        im = Image.new("RGB", (8, 8))
        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        exif2 = piexif.load(o.getvalue())
        zeroth_ifd2 = exif2["0th"]
        self.assertDictEqual(zeroth_ifd, zeroth_ifd2)

    def test_load_tif_m(self):
        with open(INPUT_FILE_TIF, "rb") as f:
            tif = f.read()
        exif = piexif.load(tif)
        zeroth_ifd = exif["0th"]
        exif_bytes = piexif.dump({"0th":zeroth_ifd})

        im = Image.new("RGB", (8, 8))
        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        exif2 = piexif.load(o.getvalue())
        zeroth_ifd2 = exif2["0th"]
        self.assertDictEqual(zeroth_ifd, zeroth_ifd2)

    def test_load_from_pilImage_property(self):
        o = io.BytesIO()
        i = Image.open(INPUT_FILE1)
        exif = i.info["exif"]
        exif_dict = piexif.load(exif)
        exif_bytes = piexif.dump(exif_dict)
        i.save(o, "jpeg", exif=exif_bytes)
        i.close()
        o.seek(0)
        Image.open(o).close()

    def test_load_name_dict(self):
        thumbnail_io = io.BytesIO()
        thumb = Image.open(INPUT_FILE2)
        thumb.thumbnail((40, 40))
        thumb.save(thumbnail_io, "JPEG")
        thumb.close()
        thumb_data = thumbnail_io.getvalue()
        exif_dict = {"0th":ZEROTH_IFD,
                     "Exif":EXIF_IFD,
                     "GPS":GPS_IFD,
                     "Interop":INTEROP_IFD,
                     "1st":FIRST_IFD,
                     "thumbnail":thumb_data}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGB", (80, 80))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = piexif.load(o.getvalue(), True)
        print(exif)

    def test_load_unicode_filename(self):
        input_file = os.path.join(u"tests", u"images", u"r_sony.jpg")
        exif = piexif.load(input_file)
        e = load_exif_by_PIL(input_file)
        self._compare_piexifDict_PILDict(exif, e, p=False)

# dump ------
    def test_no_exif_dump(self):
        o = io.BytesIO()
        exif_bytes = piexif.dump({})
        i = Image.new("RGB", (8, 8))
        i.save(o, format="jpeg", exif=exif_bytes)
        o.seek(0)
        exif_dict2 = load_exif_by_PIL(o)
        self.assertDictEqual({},  exif_dict2)

    def test_dump(self):
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        t = time.time()
        exif_bytes = piexif.dump(exif_dict)
        t_cost = time.time() - t
        print("'dump': {}[sec]".format(t_cost))
        im = Image.new("RGB", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = load_exif_by_PIL(o)

    def test_dump_fail(self):
        with open(os.path.join("tests", "images", "large.jpg"), "rb") as f:
            thumb_data = f.read()
        exif_dict = {"0th":ZEROTH_IFD,
                     "Exif":EXIF_IFD,
                     "GPS":GPS_IFD,
                     "Interop":INTEROP_IFD,
                     "1st":FIRST_IFD,
                     "thumbnail":thumb_data}
        with self.assertRaises(ValueError):
            piexif.dump(exif_dict)

    def test_dump_fail2(self):
        exif_ifd = {ExifIFD.DateTimeOriginal: 123}
        exif_dict = {"Exif":exif_ifd}
        with self.assertRaises(ValueError):
            piexif.dump(exif_dict)

    def test_dump_fail3(self):
        exif_ifd = {ExifIFD.OECF: 1}
        exif_dict = {"Exif":exif_ifd}
        with self.assertRaises(ValueError):
            piexif.dump(exif_dict)

    def test_dump_fail4(self):
        exif_ifd = {ExifIFD.OECF: (1, 2, 3, 4, 5)}
        exif_dict = {"Exif":exif_ifd}
        with self.assertRaises(ValueError):
            piexif.dump(exif_dict)

# load and dump ------
    def test_dump_and_load(self):
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGB", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = piexif.load(o.getvalue())
        zeroth_ifd, exif_ifd, gps_ifd = exif["0th"], exif["Exif"], exif["GPS"]
        zeroth_ifd.pop(ImageIFD.ExifTag) # pointer to exif IFD
        zeroth_ifd.pop(ImageIFD.GPSTag) # pointer to GPS IFD
        self.assertDictEqual(ZEROTH_IFD, zeroth_ifd)
        self.assertDictEqual(EXIF_IFD, exif_ifd)
        self.assertDictEqual(GPS_IFD, gps_ifd)

    def test_dump_and_load2(self):
        thumbnail_io = io.BytesIO()
        thumb = Image.open(INPUT_FILE2)
        thumb.thumbnail((40, 40))
        thumb.save(thumbnail_io, "JPEG")
        thumb.close()
        thumb_data = thumbnail_io.getvalue()
        exif_dict = {"0th":ZEROTH_IFD,
                     "Exif":EXIF_IFD,
                     "GPS":GPS_IFD,
                     "Interop":INTEROP_IFD,
                     "1st":FIRST_IFD,
                     "thumbnail":thumb_data}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.new("RGB", (80, 80))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        exif = piexif.load(o.getvalue())
        exif["0th"].pop(ImageIFD.ExifTag) # pointer to exif IFD
        exif["0th"].pop(ImageIFD.GPSTag) # pointer to GPS IFD
        exif["Exif"].pop(ExifIFD.InteroperabilityTag)
        self.assertDictEqual(ZEROTH_IFD, exif["0th"])
        self.assertDictEqual(EXIF_IFD, exif["Exif"])
        self.assertDictEqual(GPS_IFD, exif["GPS"])
        self.assertDictEqual(INTEROP_IFD, exif["Interop"])
        exif["1st"].pop(513) # pointer to exif IFD
        exif["1st"].pop(514) # pointer to GPS IFD
        self.assertDictEqual(FIRST_IFD, exif["1st"])
        Image.open(io.BytesIO(exif["thumbnail"])).close()

    def test_dump_and_load3(self):
        ascii_v = ["a", "ab", "abc", "abcd", "abcde"]
        undefined_v = [b"\x00",
                       b"\x00\x01",
                       b"\x00\x01\x02",
                       b"\x00\x01\x02\x03",
                       b"\x00\x01\x02\x03\x04"]
        byte_v = [255,
                  (255, 254),
                  (255, 254, 253),
                  (255, 254, 253, 252),
                  (255, 254, 253, 252, 251)]
        short_v = [65535,
                   (65535, 65534),
                   (65535, 65534, 65533),
                   (65535, 65534, 65533, 65532),
                   (65535, 65534, 65533, 65532, 65531)]
        long_v = [4294967295,
                  (4294967295, 4294967294),
                  (4294967295, 4294967294, 4294967293),
                  (4294967295, 4294967294, 4294967293, 4294967292),
                  (5, 4, 3, 2, 1)]
        rational_v = [(4294967295, 4294967294),
                      ((4294967295, 4294967294), (4294967293, 4294967292)),
                      ((1, 2), (3, 4), (5, 6)),
                      ((1, 2), (3, 4), (5, 6), (7, 8)),
                      ((1, 2), (3, 4), (5, 6), (7, 8), (9, 10))]
        srational_v = [(2147483647, -2147483648),
                       ((2147483647, -2147483648), (2147483645, 2147483644)),
                       ((1, 2), (3, 4), (5, 6)),
                       ((1, 2), (3, 4), (5, 6), (7, 8)),
                       ((1, 2), (3, 4), (5, 6), (7, 8), (9, 10))]
        for x in range(5):
            exif_dict = {
                "0th":{ImageIFD.ProcessingSoftware:ascii_v[x],
                       ImageIFD.InterColorProfile:undefined_v[x],
                       ImageIFD.SubfileType:short_v[x],
                       ImageIFD.WhitePoint:rational_v[x],
                       ImageIFD.BlackLevelDeltaH:srational_v[x]},
                "Exif":{ExifIFD.ISOSpeed:long_v[x]},
                "GPS":{GPSIFD.GPSVersionID:byte_v[x]},}
            exif_bytes = piexif.dump(exif_dict)
            e = piexif.load(exif_bytes)
            self.assertEqual(
                e["0th"][ImageIFD.ProcessingSoftware].decode("latin1"),
                ascii_v[x])
            self.assertEqual(
                e["0th"][ImageIFD.InterColorProfile], undefined_v[x])
            self.assertEqual(e["0th"][ImageIFD.SubfileType], short_v[x])
            self.assertEqual(e["0th"][ImageIFD.WhitePoint], rational_v[x])
            self.assertEqual(
                e["0th"][ImageIFD.BlackLevelDeltaH], srational_v[x])
            self.assertEqual(e["Exif"][ExifIFD.ISOSpeed], long_v[x])
            self.assertEqual(e["GPS"][GPSIFD.GPSVersionID], byte_v[x])

    def test_dump_and_load_specials(self):
        """test dump and load special types(SingedByte, SiginedShort, DoubleFloat)"""
        zeroth_ifd_original = {
            ImageIFD.ZZZTestSByte:-128,
            ImageIFD.ZZZTestSShort:-32768,
            ImageIFD.ZZZTestDFloat:1.0e-100,
        }
        exif_dict = {"0th":zeroth_ifd_original}
        exif_bytes = piexif.dump(exif_dict)

        exif = piexif.load(exif_bytes)
        zeroth_ifd = exif["0th"]
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestSByte],
            zeroth_ifd[ImageIFD.ZZZTestSByte]
        )
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestSShort],
            zeroth_ifd[ImageIFD.ZZZTestSShort]
        )
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestDFloat],
            zeroth_ifd[ImageIFD.ZZZTestDFloat]
        )

    def test_dump_and_load_specials2(self):
        """test dump and load special types(SingedByte, SiginedShort, DoubleFloat)"""
        zeroth_ifd_original = {
            ImageIFD.ZZZTestSByte:(-128, -128),
            ImageIFD.ZZZTestSShort:(-32768, -32768),
            ImageIFD.ZZZTestDFloat:(1.0e-100, 1.0e-100),
        }
        exif_dict = {"0th":zeroth_ifd_original}
        exif_bytes = piexif.dump(exif_dict)

        exif = piexif.load(exif_bytes)
        zeroth_ifd = exif["0th"]
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestSByte],
            zeroth_ifd[ImageIFD.ZZZTestSByte]
        )
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestSShort],
            zeroth_ifd[ImageIFD.ZZZTestSShort]
        )
        self.assertEqual(
            zeroth_ifd_original[ImageIFD.ZZZTestDFloat],
            zeroth_ifd[ImageIFD.ZZZTestDFloat]
        )


    def test_roundtrip_files(self):
        files = glob.glob(os.path.join("tests", "images", "r_*.jpg"))
        for input_file in files:
            print(input_file)
            exif = piexif.load(input_file)
            exif_bytes = piexif.dump(exif)
            o = io.BytesIO()
            piexif.insert(exif_bytes, input_file, o)
            e = piexif.load(o.getvalue())

            t = e.pop("thumbnail")
            thumbnail = exif.pop("thumbnail")
            if t is not None:
                if not (b"\xe0" <= thumbnail[3:4] <= b"\xef"):
                    self.assertEqual(t, thumbnail)
                else:
                    print("Given JPEG doesn't follow exif thumbnail standard. "
                            "APPn segments in thumbnail should be removed, "
                            "whereas thumbnail JPEG has it. \n: " +
                            input_file)
                exif["1st"].pop(513)
                e["1st"].pop(513)
                exif["1st"].pop(514)
                e["1st"].pop(514)
            for ifd in e:
                if ifd == "0th":
                    if ImageIFD.ExifTag in exif["0th"]:
                        exif["0th"].pop(ImageIFD.ExifTag)
                        e["0th"].pop(ImageIFD.ExifTag)
                    if ImageIFD.GPSTag in exif["0th"]:
                        exif["0th"].pop(ImageIFD.GPSTag)
                        e["0th"].pop(ImageIFD.GPSTag)
                elif ifd == "Exif":
                    if ExifIFD.InteroperabilityTag in exif["Exif"]:
                        exif["Exif"].pop(ExifIFD.InteroperabilityTag)
                        e["Exif"].pop(ExifIFD.InteroperabilityTag)
                for key in exif[ifd]:
                    self.assertEqual(exif[ifd][key], e[ifd][key])
            print(" - pass")

# transplant ------
    def test_transplant(self):
        piexif.transplant(INPUT_FILE1, INPUT_FILE_PEN, "transplant.jpg")
        i = Image.open("transplant.jpg")
        i.close()
        exif_src = piexif.load(INPUT_FILE1)
        img_src = piexif.load(INPUT_FILE_PEN)
        generated = piexif.load("transplant.jpg")
        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)

        piexif.transplant(INPUT_FILE1, "transplant.jpg")
        self.assertEqual(piexif.load(INPUT_FILE1),
                         piexif.load("transplant.jpg"))
        os.remove("transplant.jpg")

    def test_transplant_m(self):
        """'transplant' on memory.
        """
        o = io.BytesIO()
        piexif.transplant(I1, I2, o)
        self.assertEqual(piexif.load(I1), piexif.load(o.getvalue()))
        Image.open(o).close()

    def test_transplant_fail1(self):
        with  self.assertRaises(ValueError):
            piexif.transplant(I1, I2, False)

    def test_transplant_fail2(self):
        with  self.assertRaises(ValueError):
            piexif.transplant(NOEXIF_FILE, I2, "foo.jpg")

# remove ------
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

        piexif.remove("remove.jpg")
        exif_dict = piexif.load("remove.jpg")
        self.assertEqual(exif_dict, none_dict)
        os.remove("remove.jpg")

    def test_remove2(self):
        with open(INPUT_FILE1, "rb") as f:
            data = f.read()
        with open("remove2.jpg", "wb+") as f:
            f.write(data)
        piexif.remove("remove2.jpg")
        exif_dict = piexif.load("remove2.jpg")
        none_dict = {"0th":{},
                     "Exif":{},
                     "GPS":{},
                     "Interop":{},
                     "1st":{},
                     "thumbnail":None}
        self.assertEqual(exif_dict, none_dict)
        os.remove("remove2.jpg")

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

# insert ------
    def test_insert(self):
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, INPUT_FILE1, "insert.jpg")
        exif = load_exif_by_PIL("insert.jpg")

        piexif.insert(exif_bytes, NOEXIF_FILE, "insert.jpg")

        with self.assertRaises(ValueError):
            piexif.insert(b"dummy", io.BytesIO())

        piexif.insert(exif_bytes, "insert.jpg")
        os.remove("insert.jpg")

    def test_insert_m(self):
        """'insert' on memory.
        """
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        exif_bytes = piexif.dump(exif_dict)
        o = io.BytesIO()
        piexif.insert(exif_bytes, I1, o)
        self.assertEqual(o.getvalue()[0:2], b"\xff\xd8")
        exif = load_exif_by_PIL(o)

    def test_insert_fail1(self):
        with open(INPUT_FILE1, "rb") as f:
            data = f.read()
        with open("insert.jpg", "wb+") as f:
            f.write(data)
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        exif_bytes = piexif.dump(exif_dict)
        with  self.assertRaises(ValueError):
            piexif.insert(exif_bytes, INPUT_FILE_TIF)
        os.remove("insert.jpg")

    def test_insert_fail2(self):
        exif_dict = {"0th":ZEROTH_IFD, "Exif":EXIF_IFD, "GPS":GPS_IFD}
        exif_bytes = piexif.dump(exif_dict)
        with  self.assertRaises(ValueError):
            piexif.insert(exif_bytes, I1, False)

# ------
    def test_print_exif(self):
        print("\n**********************************************")
        t = time.time()
        exif = piexif.load(INPUT_FILE_PEN)
        t_cost = time.time() - t
        print("'load': {}[sec]".format(t_cost))
        for ifd in ("0th", "Exif", "GPS", "Interop", "1st"):
            print("\n{} IFD:".format(ifd))
            d = exif[ifd]
            for key in sorted(d):
                try:
                    print("  ", key, TAGS[ifd][key]["name"], d[key][:10])
                except:
                    print("  ", key, TAGS[ifd][key]["name"], d[key])
        print("**********************************************")

# test utility methods----------------------------------------------

    def _compare_value(self, v1, v2):
        if type(v1) != type(v2):
            if isinstance(v1, tuple):
                self.assertEqual(pack_byte(*v1), v2)
            elif isinstance(v1, int):
                self.assertEqual(struct.pack("B", v1), v2)
            elif isinstance(v2, int):
                self.assertEqual(struct.pack("B", v2), v1)
            elif isinstance(v1, bytes) and isinstance(v2, str):
                try:
                    self.assertEqual(v1, v2.encode("latin1"))
                except:
                    self.assertEqual(v1, v2)
            else:
                try:
                    self.assertEqual(v1, v2.encode("latin1"))
                except:
                    self.assertEqual(v1, v2)
        else:
            self.assertEqual(v1, v2)

    def _compare_piexifDict_PILDict(self, piexifDict, pilDict, p=True):
        zeroth_ifd = piexifDict["0th"]
        exif_ifd = piexifDict["Exif"]
        gps_ifd = piexifDict["GPS"]
        if 41728 in exif_ifd:
            exif_ifd.pop(41728) # value type is UNDEFINED but PIL returns int
        if 34853 in pilDict:
            gps = pilDict.pop(34853)

        for key in sorted(zeroth_ifd):
            if key in pilDict:
                self._compare_value(zeroth_ifd[key], pilDict[key])
                if p:
                    try:
                        print(TAGS["0th"][key]["name"],
                              zeroth_ifd[key][:10], pilDict[key][:10])
                    except:
                         print(TAGS["0th"][key]["name"],
                               zeroth_ifd[key], pilDict[key])
        for key in sorted(exif_ifd):
            if key in pilDict:
                self._compare_value(exif_ifd[key], pilDict[key])
                if p:
                    try:
                        print(TAGS["Exif"][key]["name"],
                              exif_ifd[key][:10], pilDict[key][:10])
                    except:
                         print(TAGS["Exif"][key]["name"],
                               exif_ifd[key], pilDict[key])
        for key in sorted(gps_ifd):
            if key in gps:
                self._compare_value(gps_ifd[key], gps[key])
                if p:
                    try:
                        print(TAGS["GPS"][key]["name"],
                              gps_ifd[key][:10], gps[key][:10])
                    except:
                         print(TAGS["GPS"][key]["name"],
                               gps_ifd[key], gps[key])


class UTests(unittest.TestCase):
    def test_ExifReader_return_unknown(self):
        b1 = b"MM\x00\x2a\x00\x00\x00\x08"
        b2 = b"\x00\x01" + b"\xff\xff\x00\x00\x00\x00" + b"\x00\x00\x00\x00"
        er = piexif._load._ExifReader(b1 + b2)
        if er.tiftag[0:2] == b"II":
            er.endian_mark = "<"
        else:
            er.endian_mark = ">"
        ifd = er.get_ifd_dict(8, "0th", True)
        self.assertEqual(ifd[65535][0], 0)
        self.assertEqual(ifd[65535][1], 0)
        self.assertEqual(ifd[65535][2], b"\x00\x00")

    def test_ExifReader_convert_value_fail(self):
        er = piexif._load._ExifReader(I1)
        with self.assertRaises(ValueError):
            er.convert_value((None, None, None, None))

    def test_split_into_segments_fail1(self):
        with self.assertRaises(InvalidImageDataError):
            _common.split_into_segments(b"I'm not JPEG")

    def test_split_into_segments_fail2(self):
        with self.assertRaises(ValueError):
            _common.split_into_segments(b"\xff\xd8\xff\xe1\xff\xff")

    def test_merge_segments(self):
        # Remove APP0, when both APP0 and APP1 exists.
        with open(INPUT_FILE1, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments)
        segments = _common.split_into_segments(new_data)
        self.assertFalse(segments[1][0:2] == b"\xff\xe0"
                        and segments[2][0:2] == b"\xff\xe1")
        self.assertEqual(segments[1][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        without_app0 = o.getvalue()
        Image.open(o).close()

        exif = _common.get_exif_seg(segments)

        # Remove Exif, when second 'merged_segments' arguments is None
        # and no APP0.
        segments = _common.split_into_segments(without_app0)
        new_data = _common.merge_segments(segments, None)
        segments = _common.split_into_segments(new_data)
        self.assertNotEqual(segments[1][0:2], b"\xff\xe0")
        self.assertNotEqual(segments[1][0:2], b"\xff\xe1")
        self.assertNotEqual(segments[2][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

        # Insert exif to jpeg that has APP0 and Exif.
        o = io.BytesIO()
        i = Image.new("RGB", (8, 8))
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

        # Insert exif to jpeg that doesn't have APP0 and Exif.
        with open(NOAPP01_FILE, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments, exif)
        segments = _common.split_into_segments(new_data)
        self.assertEqual(segments[1][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

        # Remove Exif, when second 'merged_segments' arguments is None
        # and Exif exists.
        with open(INPUT_FILE1, "rb") as f:
            original = f.read()
        segments = _common.split_into_segments(original)
        new_data = _common.merge_segments(segments, None)
        segments = _common.split_into_segments(new_data)
        self.assertNotEqual(segments[1][0:2], b"\xff\xe1")
        self.assertNotEqual(segments[2][0:2], b"\xff\xe1")
        o = io.BytesIO(new_data)
        Image.open(o).close()

    def test_dump_user_comment(self):
        # ascii
        header = b"\x41\x53\x43\x49\x49\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("ascii")
        result = helper.UserComment.dump(string, "ascii")
        self.assertEqual(binary, result)

        # jis
        header = b"\x4a\x49\x53\x00\x00\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("shift_jis")
        result = helper.UserComment.dump(string, "jis")
        self.assertEqual(binary, result)

        # unicode
        header = b"\x55\x4e\x49\x43\x4f\x44\x45\x00"
        string = u"abcd"
        binary = header + string.encode("utf-16-be")
        result = helper.UserComment.dump(string, "unicode")
        self.assertEqual(binary, result)

        # undefined
        header = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("latin")
        self.assertRaises(ValueError, helper.UserComment.dump, string, "undefined")


    def test_load_user_comment(self):
        # ascii
        header = b"\x41\x53\x43\x49\x49\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("ascii")
        result = helper.UserComment.load(binary)
        self.assertEqual(string, result)

        # jis
        header = b"\x4a\x49\x53\x00\x00\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("shift_jis")
        result = helper.UserComment.load(binary)
        self.assertEqual(string, result)

        # unicode
        header = b"\x55\x4e\x49\x43\x4f\x44\x45\x00"
        string = u"abcd"
        binary = header + string.encode("utf-16-be")
        result = helper.UserComment.load(binary)
        self.assertEqual(string, result)

        # undefined
        header = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        string = u"abcd"
        binary = header + string.encode("ascii")
        self.assertRaises(ValueError, helper.UserComment.load, binary)


class HelperTests(unittest.TestCase):
    def test_headers(self):
        """Are our headers the correct length?"""
        self.assertEqual(len(helper.UserComment._ASCII_PREFIX), helper.UserComment._PREFIX_SIZE)
        self.assertEqual(len(helper.UserComment._JIS_PREFIX), helper.UserComment._PREFIX_SIZE)
        self.assertEqual(len(helper.UserComment._UNICODE_PREFIX), helper.UserComment._PREFIX_SIZE)
        self.assertEqual(len(helper.UserComment._UNDEFINED_PREFIX), helper.UserComment._PREFIX_SIZE)

    def test_encode_ascii(self):
        """Do we encode ASCII correctly?"""
        text = 'hello world'
        expected = b'\x41\x53\x43\x49\x49\x00\x00\x00hello world'
        actual = helper.UserComment.dump(text, encoding='ascii')
        self.assertEqual(expected, actual)

    def test_decode_ascii(self):
        """Do we decode ASCII correctly?"""
        binary = b'\x41\x53\x43\x49\x49\x00\x00\x00hello world'
        expected = 'hello world'
        actual = helper.UserComment.load(binary)
        self.assertEqual(expected, actual)

    def test_encode_jis(self):
        """Do we encode JIS correctly?"""
        text = '\u3053\u3093\u306b\u3061\u306f\u4e16\u754c'
        expected = b'\x4a\x49\x53\x00\x00\x00\x00\x00' + text.encode('shift_jis')
        actual = helper.UserComment.dump(text, encoding='jis')
        self.assertEqual(expected, actual)

    def test_decode_jis(self):
        """Do we decode JIS correctly?"""
        expected = '\u3053\u3093\u306b\u3061\u306f\u4e16\u754c'
        binary = b'\x4a\x49\x53\x00\x00\x00\x00\x00' + expected.encode('shift_jis')
        actual = helper.UserComment.load(binary)
        self.assertEqual(expected, actual)

    def test_encode_unicode(self):
        """Do we encode Unicode correctly?"""
        text = '\u3053\u3093\u306b\u3061\u306f\u4e16\u754c'
        expected = b'\x55\x4e\x49\x43\x4f\x44\x45\x00' + text.encode('utf_16_be')
        actual = helper.UserComment.dump(text, encoding='unicode')
        self.assertEqual(expected, actual)

    def test_decode_unicode(self):
        """Do we decode Unicode correctly?"""
        expected = '\u3053\u3093\u306b\u3061\u306f\u4e16\u754c'
        binary = b'\x55\x4e\x49\x43\x4f\x44\x45\x00' + expected.encode('utf_16_be')
        actual = helper.UserComment.load(binary)
        self.assertEqual(expected, actual)

    def test_encode_bad_encoding(self):
        """De we gracefully handle bad input when encoding?"""
        self.assertRaises(ValueError, helper.UserComment.dump, 'hello world', 'koi-8r')

    def test_decode_bad_encoding(self):
        """De we gracefully handle bad input when decoding?"""
        self.assertRaises(ValueError, helper.UserComment.load,
                          b'\x00\x00\x00\x00\x00\x00\x00\x00hello')
        self.assertRaises(ValueError, helper.UserComment.load,
                          b'\x12\x34\x56\x78\x9a\xbc\xde\xffhello')
        self.assertRaises(ValueError, helper.UserComment.load, b'hello world')


class WebpTests(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir("tests/images/out")
        except:
            pass

    def test_merge_chunks(self):
        """Can PIL open our output WebP?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
            "pil1.webp",
            "pil2.webp",
            "pil3.webp",
            "pil_rgb.webp",
            "pil_rgba.webp",
        ]

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue

            with open(IMAGE_DIR + filename, "rb") as f:
                data = f.read()

            chunks = _webp.split(data)
            file_header = _webp.get_file_header(chunks)
            merged = _webp.merge_chunks(chunks)
            new_webp_bytes = file_header + merged
            with open(OUT_DIR + "raw_" + filename, "wb") as f:
                f.write(new_webp_bytes)
            Image.open(OUT_DIR + "raw_" + filename)

    def test_insert_exif(self):
        """Can PIL open WebP that is inserted exif?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
            "pil1.webp",
            "pil2.webp",
            "pil3.webp",
            "pil_rgb.webp",
            "pil_rgba.webp",
        ]

        exif_dict = {
            "0th":{
                piexif.ImageIFD.Software: b"PIL",
                piexif.ImageIFD.Make: b"Make",
            }
        }

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue

            with open(IMAGE_DIR + filename, "rb") as f:
                data = f.read()
            exif_bytes = piexif.dump(exif_dict)
            exif_inserted = _webp.insert(data, exif_bytes)
            with open(OUT_DIR + "i_" + filename, "wb") as f:
                f.write(exif_inserted)
            Image.open(OUT_DIR + "i_" + filename)

    def test_remove_exif(self):
        """Can PIL open WebP that is removed exif?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
            "pil1.webp",
            "pil2.webp",
            "pil3.webp",
            "pil_rgb.webp",
            "pil_rgba.webp",
        ]

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue

            with open(IMAGE_DIR + filename, "rb") as f:
                data = f.read()
            exif_removed = _webp.remove(data)
            with open(OUT_DIR + "r_" + filename, "wb") as f:
                f.write(exif_removed)
            Image.open(OUT_DIR + "r_" + filename)

    def test_get_exif(self):
        """Can we get exif from WebP?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
        ]

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue

            with open(IMAGE_DIR + filename, "rb") as f:
                data = f.read()
            exif_bytes = _webp.get_exif(data)
            self.assertEqual(exif_bytes[0:2], b"MM")

    def test_load(self):
        """Can we get exif from WebP?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
        ]

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue
            print(piexif.load(IMAGE_DIR + filename))

    def test_remove(self):
        """Can PIL open WebP that is removed exif?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
            "pil1.webp",
            "pil2.webp",
            "pil3.webp",
            "pil_rgb.webp",
            "pil_rgba.webp",
        ]

        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue
            piexif.remove(IMAGE_DIR + filename, OUT_DIR + "rr_" + filename)
            Image.open(OUT_DIR + "rr_" + filename)

    def test_insert(self):
        """Can PIL open WebP that is inserted exif?"""
        IMAGE_DIR = "tests/images/"
        OUT_DIR = "tests/images/out/"
        files = [
            "tool1.webp",
            "pil1.webp",
            "pil2.webp",
            "pil3.webp",
            "pil_rgb.webp",
            "pil_rgba.webp",
        ]

        exif_dict = {
            "0th":{
                piexif.ImageIFD.Software: b"PIL",
                piexif.ImageIFD.Make: b"Make",
            }
        }
        exif_bytes = piexif.dump(exif_dict)
        
        for filename in files:
            try:
                Image.open(IMAGE_DIR + filename)
            except:
                print("Pillow can't read {}".format(filename))
                continue
            piexif.insert(exif_bytes, IMAGE_DIR + filename, OUT_DIR + "ii_" + filename)
            Image.open(OUT_DIR + "ii_" + filename)


def suite():
    suite = unittest.TestSuite()
    suite.addTests([
        unittest.makeSuite(UTests),
        unittest.makeSuite(ExifTests),
        unittest.makeSuite(HelperTests),
        unittest.makeSuite(WebpTests),
    ])
    return suite


if __name__ == '__main__':
    unittest.main()
