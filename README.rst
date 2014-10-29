Pyxif
=====

|Build Status| |Coverage Status|

To simplify exif manipulations with python. Writing, reading, and more...
Pyxif isn't a wrapper. To everywhere with Python(function'thumbnail'
depends on PIL or Pillow).

Functions
---------

::

    dump - converts dict to exif bytes
    insert - inserts exif bytes to JPEG
    load - get exif as dict from file
    remove - removes exif from JPEG
    thumbnail - resizes proportionally without loosing exif(depend on PIL or Pillow)
    transplant - transplants exif to another JPEG

How to Use
----------

::

    zeroth_ifd = {pyxif.ZerothIFD.Make: "Canon",
                  pyxif.ZerothIFD.XResolution: (96, 1),
                  pyxif.ZerothIFD.YResolution: (96, 1),
                  pyxif.ZerothIFD.Software: "paint.net 4.0.3",
                  }

    exif_ifd = {ExifIFD.DateTimeOriginal: "2099:09:29 10:10:10",
                ExifIFD.LensMake: "LensMake",
                ExifIFD.Sharpness: 65535,
                ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1), ),
                }

    gps_ifd = {GPSIFD.GPSVersionID: 1,
               GPSIFD.GPSDateStamp: "1999:99:99 99:99:99",
               }

    # dump and insert
    exif_bytes = pyxif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    pyxif.insert(exif_bytes, "in.jpg")
    # or
    from PIL import Image
    im = Image.open("in.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)

    # load
    zeroth_dict, exif_dict, gps_dict = pyxif.load("in.jpg")

    # remove
    pyxif.remove("in.jpg")

    # thumbnail
    pyxif.thumbnail("in.jpg", "out.jpg", (80, 80))

    # transplant
    pyxif.transplant("exif_src.jpg", "image.jpg")

on GoogleAppEngine
------------------

::

    jpg_data = self.request.get("jpeg")
    output = io.BytesIO()

    # insert
    pyxif.insert(exif_bytes, jpg_data, output)

    # load
    zeroth_dict, exif_dict, gps_dict = pyxif.load(jpg_data)

    # remove
    pyxif.remove(jpg_data, output)

    # thumbnail
    pyxif.thumbnail(jpg_data, output, (80, 80))

    # transplant
    pyxif.transplant(jpg_data1, jpg_data2, output)

Depends on
----------

Function 'thumbnail' depends on PIL, or Pillow(Tested on Pillow 2.5.3).
Others don't depend on any 3rd module.

Environment
-----------

Checked on Python 2.7, 3.3, 3.4, pypy, and pypy3.

License
-------

This software is released under the MIT License, see LICENSE.txt.

.. |Build Status| image:: https://travis-ci.org/hMatoba/Pyxif.svg?branch=master
   :target: https://travis-ci.org/hMatoba/Pyxif
.. |Coverage Status| image:: https://coveralls.io/repos/hMatoba/Pyxif/badge.png?branch=master
   :target: https://coveralls.io/r/hMatoba/Pyxif?branch=master