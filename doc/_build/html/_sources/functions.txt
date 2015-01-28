=========
Functions
=========

.. note:: This document is written for using Piexif on Python 3.x.

load
----
.. py:function:: piexif.load(filename)

   Return three IFD data that are 0thIFD, ExifIFD, and GPSIFD as dict.

   :param str filename: JPEG or TIFF
   :return: 0th IFD, Exif IFD, and GPS IFD
   :rtype: dict, dict, dict

::

    zeroth_ifd = {piexif.ZerothIFD.Make: u"Canon",
                  piexif.ZerothIFD.XResolution: (96, 1),
                  piexif.ZerothIFD.YResolution: (96, 1),
                  piexif.ZerothIFD.Software: u"paint.net 4.0.3"
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
    zeroth_ifd, exif_ifd, gps_ifd = piexif.load("foo.jpg")
    for key in zeroth_dict:
        print(key, zeroth_dict[key])
    for key in exif_dict:
        print(key, exif_dict[key])
    for key in gps_dict:
        print(key, gps_dict[key])

.. py:function:: piexif.load(data)

   Return three IFD data that are 0thIFD, ExifIFD, and GPSIFD as dict.

   :param bytes data: JPEG or TIFF
   :return: 0th IFD, Exif IFD, and GPS IFD
   :rtype: dict, dict, dict

dump
----
.. py:function:: piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)

   Return exif as bytes.

   :param dict zeroth_ifd: 0th IFD as dict
   :param dict exif_ifd: Exif IFD as dict
   :param dict gps_ifd: GPS IFD as dict
   :return: exif as bytes
   :rtype: bytes

::

    exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    from PIL import Image
    im = Image.open("foo.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save("out.jpg", exif=exif_bytes)


insert
------
.. py:function:: piexif.insert(exif_bytes, filename)

   Insert exif into JPEG.

   :param bytes exif_bytes: Exif as bytes
   :param str filename: filename

::

    exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    piexif.insert(exif_bytes, "foo.jpg")

.. py:function:: piexif.insert(exif_bytes, data, output)

   Insert exif into JPEG.

   :param bytes exif_bytes: Exif as bytes
   :param bytes data: JPEG data as bytes
   :param io.BytesIO output: instance of io.BytesIO

remove
------
.. py:function:: piexif.remove(filename)

   Remove exif from JPEG.

   :param str filename: filename

::

    piexif.remove("foo.jpg")

.. py:function:: piexif.remove(data, output)

   Remove exif from JPEG.

   :param bytes data: JPEG data as bytes
   :param io.BytesIO output: instance of io.BytesIO

transplant
----------
.. py:function:: piexif.transplant(filename1, filename2)

   Transplant exif from filename1 to filename2.

   :param str filename1: filename
   :param str filename2: filename

::

    piexif.transplant("exif_src.jpg", "foo.jpg")

.. py:function:: piexif.transplant(exif_src, image_src, output)

   Transplant exif from exif_src to image_src.

   :param bytes exif_src: JPEG data as bytes
   :param bytes image_src: JPEG data as bytes
   :param io.BytesIO output: instance of io.BytesIO
