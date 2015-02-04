=========
Functions
=========

.. warning:: It could set any value in exif without actual value. For example, actual XResolution is 300, whereas XResolution value in exif is 0. Confliction might happen.
.. warning:: To edit exif tags and values appropriately, read official document from P167-. http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf
.. note:: This document is written for using Piexif on Python 3.x.


load
----
.. py:function:: piexif.load(filename)

   Return exif data as dict. Keys(IFD name), be contained, are "0th", "Exif", "GPS", "Interop", "1st", and "thumbnail". Without "thumbnail", the value is dict(tag name/tag value). "thumbnail" value is JPEG as bytes.

   :param str filename: JPEG or TIFF
   :return: Exif data({"0th":dict, "Exif":dict, "GPS":dict, "Interop":dict, "1st":dict, "thumbnail":bytes})
   :rtype: dict

::

    exif_dict = piexif.load("foo.jpg")
    thumbnail = exif_dict.pop("thumbnail")
    if thumbnail is not None:
        with open("thumbnail.jpg", "wb+") as f:
            f.write(thumbnail)    
    for ifd_name in exif_dict:
        print("\n{0} IFD:".format(ifd_name))
        for key in exif_dict[ifd_name]:
            try:
                print(key, exif_dict[ifd_name][key][:10])
            except:
                print(key, exif_dict[ifd_name][key])

.. py:function:: piexif.load(data)

   Return exif data as dict. The keys(IFD name), will be contained, are "0th", "Exif", "GPS", "Interop", "1st", and "thumbnail". If there is no data to return, the key won't be contained. Without "thumbnail", the value is dict(tag name/tag value). "thumbnail" value is JPEG as bytes.

   :param bytes data: JPEG or TIFF
   :return: Exif data({"0th":dict, "Exif":dict, "GPS":dict, "Interop":dict, "1st":dict, "thumbnail":bytes})
   :rtype: dict

dump
----

.. py:function:: piexif.dump(exif_dict)

   Return exif as bytes.

   :param dict exif_dict: Exif data({"0th":0thIFD - dict, "Exif":ExifIFD - dict, "GPS":GPSIFD - dict, "Interop":InteroperabilityIFD - dict, "1st":1stIFD - dict, "thumbnail":JPEG data - bytes})
   :return: Exif
   :rtype: bytes

::

    import io
    from PIL import Image
    import piexif

    o = io.BytesIO()
    thumb_im = Image.open("foo.jpg")
    thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
    thumb_im.save(o, "jpeg")
    thumbnail = o.getvalue()

    zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
                  piexif.ImageIFD.XResolution: (96, 1),
                  piexif.ImageIFD.YResolution: (96, 1),
                  piexif.ImageIFD.Software: u"piexif"
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
    first_ifd = {piexif.ImageIFD.Make: u"Canon",
                 piexif.ImageIFD.XResolution: (40, 1),
                 piexif.ImageIFD.YResolution: (40, 1),
                 piexif.ImageIFD.Software: u"piexif"
                 }
    
    exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd, "thumbnail":thumbnail}
    exif_bytes = piexif.dump(exif_dict)
    im = Image.open("foo.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save("out.jpg", exif=exif_bytes)

Properties of *piexif.ImageIFD* help to make 0thIFD dict and 1stIFD dict. *piexif.ExifIFD* is for ExifIFD dict. *piexif.GPSIFD* is for GPSIFD dict. *piexif.InteropIFD* is for InteroperabilityIFD dict.

.. note:: ExifTag(34665), GPSTag(34853), and InteroperabilityTag(40965) in 0thIFD automatically are set appropriate value.
.. note:: JPEGInterchangeFormat(513), and JPEGInterchangeFormatLength(514) in 1stIFD automatically are set appropriate value.
.. note:: If 'thumbnail' is contained in dict, '1st' must be contained -- and vice versa. 1stIFD means thumbnail's information.

insert
------
.. py:function:: piexif.insert(exif_bytes, filename)

   Insert exif into JPEG.

   :param bytes exif_bytes: Exif as bytes
   :param str filename: JPEG

::

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, "foo.jpg")

.. py:function:: piexif.insert(exif_bytes, data, output)

   Insert exif into JPEG.

   :param bytes exif_bytes: Exif as bytes
   :param bytes data: JPEG data
   :param io.BytesIO output: ouput data

remove
------
.. py:function:: piexif.remove(filename)

   Remove exif from JPEG.

   :param str filename: JPEG

::

    piexif.remove("foo.jpg")

.. py:function:: piexif.remove(data, output)

   Remove exif from JPEG.

   :param bytes data: JPEG data
   :param io.BytesIO output: output data

transplant
----------
.. py:function:: piexif.transplant(filename1, filename2)

   Transplant exif from filename1 to filename2.

   :param str filename1: JPEG
   :param str filename2: JPEG

::

    piexif.transplant("exif_src.jpg", "foo.jpg")

.. py:function:: piexif.transplant(exif_src, image_src, output)

   Transplant exif from exif_src to image_src.

   :param bytes exif_src: JPEG data
   :param bytes image_src: JPEG data
   :param io.BytesIO output: output data
