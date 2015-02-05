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
from piexif import _common, ImageIFD, ExifIFD, GPSIFD, TAGS


print("piexif version: {0}".format(piexif.VERSION))


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


ZEROTH_DICT = {ImageIFD.Software: b"PIL", # ascii
               ImageIFD.Make: b"Make", # ascii
               ImageIFD.Model: b"XXX-XXX", # ascii
               ImageIFD.ResolutionUnit: 65535, # short
               ImageIFD.BitsPerSample: (24, 24, 24), # short * 3
               ImageIFD.XResolution: (4294967295, 1), # rational
               ImageIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1)), # srational
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
        os.remove("transplant.jpg")

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

    def test_load(self):
        for input_file in (os.path.join("tests", "images", "r_canon.jpg"),
                           os.path.join("tests", "images", "r_ricoh.jpg")):
            exif = piexif.load(input_file)
            e = load_exif_by_PIL(input_file)
            self._compare_piexifDict_PILDict(exif, e)

    def test_load_m(self):
        """'load' on memory.
        """
        exif = piexif.load(I1)
        e = load_exif_by_PIL(INPUT_FILE1)
        self._compare_piexifDict_PILDict(exif, e)

    def test_dump(self):
        exif_dict = {"0th":ZEROTH_DICT, "Exif":EXIF_DICT, "GPS":GPS_DICT}
        t = time.time()
        exif_bytes = piexif.dump(exif_dict)
        t_cost = time.time() - t
        print("'dump': {0}[sec]".format(t_cost))
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
        os.remove("insert.jpg")

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
        exif2 = piexif.load(o.getvalue())
        zeroth_ifd2 = exif2["0th"]
        self.assertDictEqual(zeroth_ifd, zeroth_ifd2)

    def test_dump_and_load_2(self):
        thumbnail_io = io.BytesIO()
        thumb = Image.open(INPUT_FILE2)
        thumb.thumbnail((40, 40))
        thumb.save(thumbnail_io, "JPEG")
        thumb.close()
        thumb_data = thumbnail_io.getvalue()
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
        Image.open(io.BytesIO(exif["thumbnail"])).close()

    def test_roundtrip_files(self):
        files = glob.glob(os.path.join("tests", "images", "*.jpg"))
        for input_file in files:
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
                    if ImageIFD.InteroperabilityPointer in exif["0th"]:
                        exif["0th"].pop(ImageIFD.InteroperabilityPointer)
                        e["0th"].pop(ImageIFD.InteroperabilityPointer)
                for key in exif[ifd]:
                    self.assertEqual(exif[ifd][key], e[ifd][key])

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

    def test_print_exif(self):
        print("\n**********************************************")
        t = time.time()
        exif = piexif.load(INPUT_FILE_PEN)
        t_cost = time.time() - t
        print("'load': {0}[sec]".format(t_cost))
        for ifd in ("0th", "Exif", "GPS", "Interop", "1st"):
            print("\n{0} IFD:".format(ifd))
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
                self.assertEqual(v1, v2)
        else:
            self.assertEqual(v1, v2)

    def _compare_piexifDict_PILDict(self, piexifDict, pilDict):
        zeroth_dict = piexifDict["0th"]
        exif_dict = piexifDict["Exif"]
        gps_dict = piexifDict["GPS"]
        if 41728 in exif_dict:
            exif_dict.pop(41728) # value type is UNDEFINED but PIL returns int
        if 34853 in pilDict:
            gps = pilDict.pop(34853)
        counter = {"Byte":0, "Ascii":0, "Short":0, "Long":0, "Rational":0, 
                   "SRational":0, "Undefined":0}
        for key in sorted(zeroth_dict):
            if key in pilDict:
                self._compare_value(zeroth_dict[key], pilDict[key])
                t = TAGS["0th"][key]["type"]
                counter[t] += 1
        for key in sorted(exif_dict):
            if key in pilDict:
                self._compare_value(exif_dict[key], pilDict[key])
                t = TAGS["Exif"][key]["type"]
                counter[t] += 1
        for key in sorted(gps_dict):
            if key in gps:
                self._compare_value(gps_dict[key], gps[key])
                t = TAGS["GPS"][key]["type"]
                counter[t] += 1
        print(counter)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ExifTests))
    return suite


if __name__ == '__main__':
    unittest.main()