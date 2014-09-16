import io
import os
import unittest

from PIL import Image
import pyxif


print(pyxif.VERSION)

INPUT_FILE1 = os.path.join("samples", "01.jpg")
INPUT_FILE2 = os.path.join("samples", "02.jpg")
NOEXIF_FILE = os.path.join("samples", "noexif.jpg")

with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()
with open(INPUT_FILE2, "rb") as f:
    I2 = f.read()

class ExifTests(unittest.TestCase):
    def test_transplant(self):
        pyxif.transplant(INPUT_FILE1,
                         INPUT_FILE2,
                         os.path.join("samples", "transplant.jpg"))
        exif_src = pyxif.load(INPUT_FILE1)
        img_src = pyxif.load(INPUT_FILE2)
        generated = pyxif.load(os.path.join("samples", "transplant.jpg"))

        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)
        with  self.assertRaises(ValueError):
            pyxif.transplant(NOEXIF_FILE,
                             INPUT_FILE2,
                             os.path.join("samples", "foo.jpg"))

    def test_transplant2(self):
        """To use on server.
        Passes binary data to input,
        and passes io.BytesIO instance to output
        """
        o = io.BytesIO()
        pyxif.transplant(I1, I2, o)
        self.assertEqual(pyxif.load(I1), pyxif.load(o.getvalue()))

    def test_remove(self):
        pyxif.remove(INPUT_FILE1, os.path.join("samples", "remove.jpg"))
        exif = pyxif.load(os.path.join("samples", "remove.jpg"))[0]
        self.assertEqual(exif, {})

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

    def test_thumbnail(self):
        e1 = pyxif.load(INPUT_FILE1)
        pyxif.thumbnail(INPUT_FILE1, os.path.join("samples", "thumbnail.jpg"), (50, 50))
        e2 = pyxif.load(os.path.join("samples", "thumbnail.jpg"))
        self.assertEqual(e1, e2)

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

    def test_load(self):
        input_file = INPUT_FILE1
        zeroth_dict, exif_dict, gps_dict = pyxif.load(input_file)
        self.assertEqual(zeroth_dict[272][1].decode("utf-8"), "QV-R51 ")
        self.assertEqual(zeroth_dict[296][1], 2)
        self.assertEqual(zeroth_dict[282][1], (72, 1))

    def test_load2(self):
        """To use on server.
        Passes binary data to input.
        """
        zeroth_dict, exif_dict, gps_dict = pyxif.load(I1)
        self.assertEqual(zeroth_dict[272][1].decode("utf-8"), "QV-R51 ")
        self.assertEqual(zeroth_dict[296][1], 2)
        self.assertEqual(zeroth_dict[282][1], (72, 1))

    def test_dump(self):
        input_file = INPUT_FILE1
        output_file = os.path.join("samples", "dump.jpg")
        zeroth_ifd = {282: (96, 1),
                      283: (96, 1),
                      296: 2,
                      305: 'paint.net 4.0.3'}

        exif_bytes = pyxif.dump(zeroth_ifd)

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
        zeroth_ifd = {282: (96, 1),
                      283: (96, 1),
                      296: 2,
                      305: 'paint.net 4.0.3'}
        exif_bytes = pyxif.dump(zeroth_ifd)
        pyxif.insert(exif_bytes, INPUT_FILE1, os.path.join("samples", "insert.jpg"))
        try:
            i = Image.open(os.path.join("samples", "insert.jpg"))
            i._getexif()
        except:
            self.fail("'insert' generated bad exif")
        finally:
            i.close()

    def test_insert2(self):
        """To use on server.
        Passes binary data to input.
        """
        zeroth_ifd = {282: (96, 1),
                      283: (96, 1),
                      296: 2,
                      305: 'paint.net 4.0.3'}
        exif_bytes = pyxif.dump(zeroth_ifd)
        o = io.BytesIO()
        pyxif.insert(exif_bytes, INPUT_FILE1, o)
        self.assertEqual(o.getvalue()[0:2], b"\xff\xd8")


if __name__ == '__main__':
    unittest.main()
