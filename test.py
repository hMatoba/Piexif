import io
import os
import unittest

from PIL import Image
import pyxif

ImageGroup = pyxif.ImageGroup
PhotoGroup = pyxif.PhotoGroup
GPSGroup = pyxif.GPSInfoGroup

print("Pyxif version: {0}".format(pyxif.VERSION))

INPUT_FILE1 = os.path.join("samples", "01.jpg")
INPUT_FILE2 = os.path.join("samples", "02.jpg")
INPUT_FILE_LE1 = os.path.join("samples", "L01.jpg")
NOEXIF_FILE = os.path.join("samples", "noexif.jpg")

with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()
with open(INPUT_FILE2, "rb") as f:
    I2 = f.read()

ZEROTH_DICT = {ImageGroup.Software: "PIL", # ascii
               ImageGroup.Make: "Make", # ascii
               ImageGroup.Model: "XXX-XXX", # ascii
               ImageGroup.ResolutionUnit: 65535, # short
               ImageGroup.JPEGInterchangeFormatLength: 4294967295, # long
               ImageGroup.XResolution: (4294967295, 1), # rational
               }

EXIF_DICT = {PhotoGroup.DateTimeOriginal: "2099:09:29 10:10:10", # ascii
             PhotoGroup.LensMake: "LensMake", # ascii
             PhotoGroup.Sharpness: 65535, # short
             PhotoGroup.ISOSpeed: 4294967295, # long
             PhotoGroup.ExposureTime: (4294967295, 1), # rational
             PhotoGroup.ExposureBiasValue: (2147483647, -2147483648), # srational
             }

GPS_DICT = {GPSGroup.GPSVersionID: 255, # byte
            GPSGroup.GPSDateStamp: "1999:99:99 99:99:99", # ascii
            GPSGroup.GPSDifferential: 65535, # short
            GPSGroup.GPSLatitude: (4294967295, 1), # rational
            }


class ExifTests(unittest.TestCase):
    def test_transplant(self):
        pyxif.transplant(INPUT_FILE1, INPUT_FILE2, "transplant.jpg")
        exif_src = pyxif.load(INPUT_FILE1)
        img_src = pyxif.load(INPUT_FILE2)
        generated = pyxif.load("transplant.jpg")

        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)
        try:
            i = Image.open("transplant.jpg")
            i._getexif()
        except:
            self.fail("'transplant' generated wrong file")
        finally:
            i.close()

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
        try:
            i = Image.open(o)
            i._getexif()
        except:
            self.fail("'transplant' generated wrong file")
        finally:
            i.close()

    def test_remove(self):
        pyxif.remove(INPUT_FILE1, "remove.jpg")
        exif = pyxif.load("remove.jpg")[0]
        self.assertEqual(exif, {})
        try:
            i = Image.open("remove.jpg")
            i._getexif()
        except:
            self.fail("'remove' generated wrong file")
        finally:
            i.close()

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
        try:
            i = Image.open(o)
            i._getexif()
        except:
            self.fail("'remove' generated wrong file")
        finally:
            i.close()

    def test_thumbnail(self):
        e1 = pyxif.load(INPUT_FILE1)
        pyxif.thumbnail(INPUT_FILE1, "thumbnail.jpg", (50, 50))
        e2 = pyxif.load("thumbnail.jpg")
        self.assertEqual(e1, e2)
        try:
            i = Image.open("thumbnail.jpg")
            i._getexif()
        except:
            self.fail("'thumbnail' generated wrong file")
        finally:
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
        try:
            i = Image.open(o)
            i._getexif()
        except:
            self.fail("'thumbnail' generated wrong file")
        finally:
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
        input_file = INPUT_FILE1
        output_file = "dump.jpg"
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)

        im = Image.open(input_file)
        im.thumbnail((100, 100), Image.ANTIALIAS)
        im.save(output_file, exif=exif_bytes)
        im.close()
        try:
            i = Image.open(output_file)
            i._getexif()
        except:
            self.fail("'dump' generated bad exif")
        finally:
            i.close()

    def test_insert(self):
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        pyxif.insert(exif_bytes, INPUT_FILE1, "insert.jpg")
        try:
            i = Image.open("insert.jpg")
            i._getexif()
        except:
            self.fail("'insert' generated wrong file")
        finally:
            i.close()

    def test_insert2(self):
        """To use on server.
        Passes binary data to input.
        """
        exif_bytes = pyxif.dump(ZEROTH_DICT, EXIF_DICT, GPS_DICT)
        o = io.BytesIO()
        pyxif.insert(exif_bytes, I1, o)
        self.assertEqual(o.getvalue()[0:2], b"\xff\xd8")
        try:
            i = Image.open(o)
            i._getexif()
        except:
            self.fail("'insert' generated wrong file")
        finally:
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


if __name__ == '__main__':
    unittest.main()
