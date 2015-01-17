Pyxif
=====

|Build Status| |Coverage Status|

| To simplify exif manipulations with python. Writing, reading, and more...
| Pyxif isn't a wrapper. To everywhere with Python.

Functions
---------

::

    load - get exif as dict from file(JPEG and TIFF)
    dump - converts dict to exif bytes
    insert - inserts exif bytes to JPEG
    remove - removes exif from JPEG
    transplant - transplants exif to another JPEG

How to Use
----------

::

    zeroth_ifd = {pyxif.ZerothIFD.Make: u"Canon",
                  pyxif.ZerothIFD.XResolution: (96, 1),
                  pyxif.ZerothIFD.YResolution: (96, 1),
                  pyxif.ZerothIFD.Software: u"paint.net 4.0.3",
                  }

    exif_ifd = {pyxif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
                pyxif.ExifIFD.LensMake: u"LensMake",
                pyxif.ExifIFD.Sharpness: 65535,
                pyxif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                }

    gps_ifd = {pyxif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
               pyxif.GPSIFD.GPSAltitudeRef: 1,
               pyxif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
               }

    # dump and insert
    exif_bytes = pyxif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    pyxif.insert(exif_bytes, "in.jpg")

    # with Pillow
    from PIL import Image
    im = Image.open("in.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)

    # load
    zeroth_dict, exif_dict, gps_dict = pyxif.load("in.jpg")

    # remove
    pyxif.remove("in.jpg")

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

    # transplant
    pyxif.transplant(jpg_data1, jpg_data2, output)

Tag Name and Value Type
-----------------------

| Each exif tag has appropriate type of the value. BYTE, ASCII, SHORT, or...
| See the document of Exif.
| http://www.kodak.com/global/plugins/acrobat/en/service/digCam/exifStandard2.pdf
| Some examples are shown below.

::

    BYTE: {GPSIFD.GPSAltitudeRef: 1}
    ASCII: {ZerothIFD.Make: u"Make"}
    SHORT: {ZerothIFD.ResolutionUnit: 65535}
    SHORT(length:3): {ZerothIFD.BitsPerSample: (24, 24, 24)}
    LONG: {ZerothIFD.JPEGInterchangeFormatLength: 4294967295}
    RATIONAL: {ZerothIFD.XResolution: (4294967295, 1)}
    UNDEFINED: {ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa"}
    SRATIONAL(length:3): {ZerothIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1))}

Depends on
----------

Pyxif doesn't depend on any 3rd module.

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