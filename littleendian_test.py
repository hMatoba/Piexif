import io
import os
import unittest

from PIL import Image
import pyxif


print("Pyxif version: {0}".format(pyxif.VERSION))

INPUT_FILE1 = os.path.join("samples", "L01.jpg")

with open(INPUT_FILE1, "rb") as f:
    I1 = f.read()


class ExifTests(unittest.TestCase):
    def test_load(self):
        input_file = INPUT_FILE1
        zeroth_dict, exif_dict, gps_dict = pyxif.load(input_file)
        self.assertEqual(zeroth_dict[272][1], "QV-R51 ")
        self.assertEqual(zeroth_dict[296][1], 2)
        self.assertEqual(zeroth_dict[282][1], (72, 1))
        self.assertEqual(exif_dict[33434][1], (1, 250))


if __name__ == '__main__':
    unittest.main()
