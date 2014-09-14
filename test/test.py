"from pyxif.test import test"

import unittest

from PIL import Image
import pyxif

INPUT_FILE1 = r'samples\01.jpg'

class ExifTests(unittest.TestCase):
    def test_transplant(self):
        pyxif.transplant(r'samples\01.jpg',
                         r'samples\02.jpg',
                         r'samples\transplant.jpg')
        exif_src = pyxif.load(r'samples\01.jpg')
        img_src = pyxif.load(r'samples\02.jpg')
        generated = pyxif.load(r'samples\transplant.jpg')

        self.assertEqual(exif_src, generated)
        self.assertNotEqual(img_src, generated)
        with  self.assertRaises(ValueError):
            pyxif.transplant(r'samples\noexif.jpg',
                             r'samples\02.jpg',
                             r'samples\foo.jpg')

    def test_remove(self):
        pyxif.remove(r"samples\01.jpg", r"samples\remove.jpg")
        exif = pyxif.load(r"samples\remove.jpg")[0]
        self.assertEqual(exif, {})

    def test_thumbnail(self):
        e1 = pyxif.load(INPUT_FILE1)
        pyxif.thumbnail(INPUT_FILE1, r"samples\thumbnail.jpg", (50, 50))
        e2 = pyxif.load(r"samples\thumbnail.jpg")
        self.assertEqual(e1, e2)

    def test_read(self):
        input_file = r"samples\01.jpg"
        zeroth_dict, exif_dict, gps_dict = pyxif.load(input_file)
        self.assertEqual(zeroth_dict[272][1].decode("utf-8"), "QV-R51 ")
        self.assertEqual(zeroth_dict[296][1], 2)
        self.assertEqual(zeroth_dict[282][1], (72, 1))

    def test_write(self):
        input_file = r"samples\01.jpg"
        output_file = r"samples\dump.jpg"
        zeroth_ifd = {282: (96, 1),
                      283: (96, 1),
                      296: 2,
                      305: 'paint.net 4.0.3'}

        exif_bytes = pyxif.dump(zeroth_ifd=zeroth_ifd)

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


if __name__ == '__main__':
    unittest.main()
