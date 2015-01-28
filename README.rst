Piexif
======

|Build Status| |Coverage Status|

| This is a renamed project from Pyxif.
| To simplify exif manipulations with python. Writing, reading, and more...
| Piexif isn't a wrapper. To everywhere with Python.

Install
-------

'easy_install'
::
    $ easy_install piexif
    
or 'pip'
::
    $ pip install --pre piexif
    
or download .zip, extract it and run
::
    $ python setup.py install

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

    zeroth_ifd = {piexif.ZerothIFD.Make: u"Canon",
                  piexif.ZerothIFD.XResolution: (96, 1),
                  piexif.ZerothIFD.YResolution: (96, 1),
                  piexif.ZerothIFD.Software: u"paint.net 4.0.3",
                  }

    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
                piexif.ExifIFD.LensMake: u"LensMake",
                piexif.ExifIFD.Sharpness: 65535,
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                }

    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
               piexif.GPSIFD.GPSAltitudeRef: 1,
               piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
               }

    # dump and insert
    exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    piexif.insert(exif_bytes, "in.jpg")

    # with Pillow
    from PIL import Image
    im = Image.open("in.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)

    # load
    zeroth_dict, exif_dict, gps_dict = piexif.load("in.jpg")

    # remove
    piexif.remove("in.jpg")

    # transplant
    piexif.transplant("exif_src.jpg", "image.jpg")

on GoogleAppEngine
------------------

::

    jpg_data = self.request.get("jpeg")
    output = io.BytesIO()

    # insert
    piexif.insert(exif_bytes, jpg_data, output)

    # load
    zeroth_dict, exif_dict, gps_dict = piexif.load(jpg_data)

    # remove
    piexif.remove(jpg_data, output)

    # transplant
    piexif.transplant(jpg_data1, jpg_data2, output)

Tag Name and Value Type
-----------------------

| Each exif tag has appropriate type of the value. BYTE, ASCII, SHORT, or...
| See the document of Exif.
| http://www.kodak.com/global/plugins/acrobat/en/service/digCam/exifStandard2.pdf
| Some examples are shown below. If value type is number and count is two or more,
| use tuple.

::

    BYTE: {GPSIFD.GPSAltitudeRef: 1}
    ASCII: {ZerothIFD.Make: u"Make"}
    SHORT: {ZerothIFD.ResolutionUnit: 65535}
    SHORT(count:3): {ZerothIFD.BitsPerSample: (24, 24, 24)}
    LONG: {ZerothIFD.JPEGInterchangeFormatLength: 4294967295}
    RATIONAL: {ZerothIFD.XResolution: (4294967295, 1)}
    UNDEFINED: {ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa"}
    SRATIONAL(count:3): {ZerothIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1))}

Depends on
----------

Piexif doesn't depend on any 3rd module.

Environment
-----------

| Tested on Python 2.7, 3.3, 3.4, pypy, and pypy3.
| Piexif would run even on IronPython.

License
-------

This software is released under the MIT License, see LICENSE.txt.

.. |Build Status| image:: https://travis-ci.org/hMatoba/Piexif.svg?branch=master
   :target: https://travis-ci.org/hMatoba/Piexif
.. |Coverage Status| image:: https://coveralls.io/repos/hMatoba/Piexif/badge.svg?branch=master
   :target: https://coveralls.io/r/hMatoba/Piexif?branch=master
