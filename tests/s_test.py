import io
import os
import sys
import unittest

from PIL import Image
import pyxif


ZerothIFD = pyxif.ZerothIFD
ExifIFD = pyxif.ExifIFD
GPSIFD = pyxif.GPSIFD

print("Pyxif version: {0}".format(pyxif.VERSION))

INPUT_FILE1 = os.path.join("tests", "images", "01.jpg")
INPUT_FILE2 = os.path.join("tests", "images", "02.jpg")
INPUT_FILE_LE1 = os.path.join("tests", "images", "L01.jpg")
NOEXIF_FILE = os.path.join("tests", "images", "noexif.jpg")

with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()
with open(INPUT_FILE2, "rb") as f:
    I2 = f.read()

ZEROTH_DICT = {ZerothIFD.Software: "PIL", # ascii
               ZerothIFD.Make: "Make", # ascii
               ZerothIFD.Model: "XXX-XXX", # ascii
               ZerothIFD.JPEGTables: b"\xaa\xaa",  # undefined
               ZerothIFD.ResolutionUnit: 65535, # short
               ZerothIFD.JPEGInterchangeFormatLength: 4294967295, # long
               ZerothIFD.XResolution: (4294967295, 1), # rational
               ZerothIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1), ),  # srational
               }

EXIF_DICT = {ExifIFD.DateTimeOriginal: "2099:09:29 10:10:10", # ascii
             ExifIFD.LensMake: "LensMake", # ascii
             ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa",  # undefined
             ExifIFD.Sharpness: 65535, # short
             ExifIFD.ISOSpeed: 4294967295, # long
             ExifIFD.ExposureTime: (4294967295, 1), # rational
             ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1), ),
             ExifIFD.ExposureBiasValue: (2147483647, -2147483648), # srational
             }

GPS_DICT = {GPSIFD.GPSVersionID: 255, # byte
            GPSIFD.GPSDateStamp: "1999:99:99 99:99:99", # ascii
            GPSIFD.GPSDifferential: 65535, # short
            GPSIFD.GPSLatitude: (4294967295, 1), # rational
            }


class ExifTests(unittest.TestCase):
    def test_no_exif_load(self):
        z, e, g = pyxif.load(NOEXIF_FILE)
        self.assertDictEqual(z, {})
        self.assertDictEqual(e, {})
        self.assertDictEqual(g, {})

    def test_no_exif_dump(self):
        s = pyxif.dump({}, {}, {})

    def test_transplant(self):
        pyxif.transplant(INPUT_FILE1, INPUT_FILE2, "transplant.jpg")
        exif_src = pyxif.load(INPUT_FILE1)
        img_src = pyxif.load(INPUT_FILE2)
        generated = pyxif.load("transplant.jpg")

        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)
        i = Image.open("transplant.jpg")
        i._getexif()
        i.close()

        pyxif.transplant(INPUT_FILE1, "transplant.jpg")

        with  self.assertRaises(ValueError):
            pyxif.transplant(NOEXIF_FILE, INPUT_FILE2, "foo.jpg")


    def test_transplant2(self):
        """To use on server.
        Passes binary data to input,
        and passes io.BytesIO instance to output
        """
        o = io.BytesIO()
        pyxif.transplant(I1, I2, o)
        self.assertEqual(pyxif.load(I1), pyxif.load(o.getvalue()))
        i = Image.open(o)
        i._getexif()
        i.close()

    def test_remove(self):
        pyxif.remove(INPUT_FILE1, "remove.jpg")
        exif = pyxif.load("remove.jpg")[0]
        self.assertEqual(exif, {})
        i = Image.open("remove.jpg")
        i._getexif()
        i.close()
        pyxif.remove("remove.jpg")

    def test_remove2(self):
        """To use on server.
        Passes binary data to input,
        and passes io.BytesIO instance to output
        """
        o = io.BytesIO()
        with  self.assertRaises(ValueError):
            pyxif.remove(I1)
        pyxif.remove(I1, o)
        exif = pyxif.load(o.getvalue())
        self.assertEqual(exif, ({}, {}, {}))
        i = Image.open(o)
        i._getexif()
        i.close()

    def test_thumbnail(self):
        e1 = pyxif.load(INPUT_FILE1)
        pyxif.thumbnail(INPUT_FILE1, "thumbnail.jpg", (50, 50))
        e2 = pyxif.load("thumbnail.jpg")
        self.assertEqual(e1, e2)
        i = Image.open("thumbnail.jpg")
        i._getexif()
        i.close()

    def test_thumbnail2(self):
        """To use on server.
        Passes binary data to input,
        and passes io.BytesIO instance to output
        """
        o = io.BytesIO()
        pyxif.thumbnail(I1, o, (50, 50))
        e1 = pyxif.load(I1)[0]
        e2 = pyxif.load(o.getvalue())[0]
        self.assertEqual(e1, e2)
        o.seek(0)
        i = Image.open(o)
        i._getexif()
        i.close()

    def test_load(self):
        zeroth_dict, exif_dict, gps_dict = pyxif.load(INPUT_FILE1)
        exif_dict.pop(41728) # value type is UNDEFINED but PIL returns int
        i = Image.open(INPUT_FILE1)
        e = i._getexif()
        i.close()
        for key in sorted(zeroth_dict):
            if key in e:
                self.assertEqual(zeroth_dict[key][1], e[key])
        for key in sorted(exif_dict):
            if key in e:
                self.assertEqual(exif_dict[key][1], e[key])
        for key in sorted(gps_dict):
            if key in e:
                self.assertEqual(gps_dict[key][1], e[key])

    def test_load2(self):
        """To use on server.
        Passes binary data to input.
        """
        zeroth_dict, exif_dict, gps_dict = pyxif.load(I1)
        self.assertEqual(zeroth_dict[272][1], "QV-R51 ")
        self.assertEqual(zeroth_dict[296][1], 2)
        self.assertEqual(zeroth_dict[282][1], (72, 1))

    def test_dump(self):
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        im = Image.new("RGBA", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        i = Image.open(o)
        i._getexif()
        i.close()

    def test_insert(self):
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        pyxif.insert(exif_bytes, INPUT_FILE1, "insert.jpg")
        i = Image.open("insert.jpg")
        i._getexif()
        i.close()

        pyxif.insert(exif_bytes, NOEXIF_FILE, "insert.jpg")

        with self.assertRaises(ValueError):
            pyxif.insert(b"dummy", io.BytesIO())

        pyxif.insert(exif_bytes, "insert.jpg")

    def test_insert2(self):
        """To use on server.
        Passes binary data to input.
        """
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        o = io.BytesIO()
        pyxif.insert(exif_bytes, I1, o)
        self.assertEqual(o.getvalue()[0:2], b"\xff\xd8")
        i = Image.open(o)
        e = i._getexif()
        i.close()

    def test_load_le(self):
        """load test of little endian exif
        """
        zeroth_dict, exif_dict, gps_dict = pyxif.load(INPUT_FILE_LE1)
        exif_dict.pop(41728) # value type is UNDEFINED but PIL returns int
        i = Image.open(INPUT_FILE_LE1)
        e = i._getexif()
        i.close()
        for key in sorted(zeroth_dict):
            if key in e:
                self.assertEqual(zeroth_dict[key][1], e[key])
        for key in sorted(exif_dict):
            if key in e:
                self.assertEqual(exif_dict[key][1], e[key])
        for key in sorted(gps_dict):
            if key in e:
                self.assertEqual(gps_dict[key][1], e[key])

    def test_dump_and_load(self):
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        im = Image.new("RGBA", (8, 8))

        o = io.BytesIO()
        im.save(o, format="jpeg", exif=exif_bytes)
        im.close()
        o.seek(0)
        pyxif.load(o.getvalue())


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ExifTests))
    return suite


if __name__ == '__main__':
    unittest.main()