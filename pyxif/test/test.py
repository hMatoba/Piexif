#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
print(os.getcwd())
if os.getcwd().endswith("test"):
    chdir("..")

import unittest

from PIL import Image
import exiftools


##class ExifTests(unittest.TestCase):
##    def test_transplant(self):
##        transplant_exif.transplant(r'samples\01.jpg',
##                                   r'samples\02.jpg',
##                                   r'samples\new.jpg')
##        exif_src = Image.open(r'samples\01.jpg')._getexif()
##        img_src = Image.open(r'samples\02.jpg')._getexif()
##        generated = Image.open(r'samples\new.jpg')._getexif()
##
##        self.assertEqual(exif_src, generated)
##        self.assertNotEquals(img_src, generated)
##        with  self.assertRaises(ValueError):
##            transplant_exif.transplant(
##                    r'samples\noexif.jpg',
##                    r'samples\02.jpg',
##                    r'samples\foo.jpg')
##
##if __name__ == "__main__":
##    unittest.main()


def read_test(input_file):
    zeroth_dict, exif_dict, gps_dict = exiftools.load_from_file(input_file)

    print("0th IFD: {0}".format(len(zeroth_dict)))
    for key in zeroth_dict:
        print(key, zeroth_dict[key])

    print("\nEXIF IFD: {0}".format(len(exif_dict)))
    for key in exif_dict:
        if isinstance(exif_dict[key][1], (str, bytes)) and len(exif_dict[key][1]) > 30:
            print(key, exif_dict[key][0], exif_dict[key][1][:10] + "...", len(exif_dict[key][1]))
        else:
            print(key, exif_dict[key])

    print("\nGPS IFD: {0}".format(len(gps_dict)))
    for key in gps_dict:
        if isinstance(gps_dict[key][1], (str, bytes)) and len(gps_dict[key][1]) > 30:
            print(key, gps_dict[key][0][:10], gps_dict[key][1][:10] + "...", len(exif_dict[key][1]))
        else:
            print(key, gps_dict[key])


def write_test(input_file, output_file):
    zeroth_ifd = {282: (96, 1),
                  283: (96, 1),
                  296: 2,
                  305: 'paint.net 4.0.3'}

    exif_bytes = exiftools.dump(zeroth_ifd=zeroth_ifd)

    im = Image.open(input_file)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)

    i = Image.open(output_file)
    print(i._getexif())


if __name__ == "__main__":
    read_test("01.jpg")
    write_test("01.jpg", "new.jpg")
