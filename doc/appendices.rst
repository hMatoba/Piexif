==========
Appendices
==========

Exif Data in Piexif
-------------------

Each exif tag has an appropriate data type (BYTE, ASCII, SHORT, etc.). Please see the official Exif standards for full documentation:
http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf

+---------------+----------------------+
| **Exif Type** | **Python Type(3.x)** |
+---------------+----------------------+
| BYTE          | int                  |
+---------------+----------------------+
| SIGNED BYTE   | int                  |
+---------------+----------------------+
| ASCII         | str                  |
+---------------+----------------------+
| SHORT         | int                  |
+---------------+----------------------+
| SIGNED SHORT  | int                  |
+---------------+----------------------+
| LONG          | int                  |
+---------------+----------------------+
| RATIONAL      | (int, int)           |
+---------------+----------------------+
| UNDEFINED     | bytes                |
+---------------+----------------------+
| SRATIONAL     | (int, int)           |
+---------------+----------------------+
| FLOAT         | float                |
+---------------+----------------------+
| DOUBLE        | float                |
+---------------+----------------------+

Values that are numerical (BYTE, SHORT, LONG, RATIONAL, or SRATIONAL) and that require two or more values should be expressed with a tuple.

+---------------------+-------------------------------+
| BYTE, SHORT, LONG   | (int, int, ...)               |
+---------------------+-------------------------------+
| RATIONAL, SRATIONAL | ((int, int), (int, int), ...) |
+---------------------+-------------------------------+

.. note:: If the value type is numerical but only one value is required, a tuple of length 1 (e.g. (int,)) is also acceptable. 


Exif in piexif example is below.

::

    zeroth_ifd = {piexif.ImageIFD.Make: "Canon",  # ASCII, count any
                  piexif.ImageIFD.XResolution: (96, 1),  # RATIONAL, count 1
                  piexif.ImageIFD.YResolution: (96, 1),  # RATIONAL, count 1
                  piexif.ImageIFD.Software: "piexif"  # ASCII, count any
                  }
    exif_ifd = {piexif.ExifIFD.ExifVersion: b"\x02\x00\x00\x00"  # UNDEFINED, count 4
                piexif.ExifIFD.LensMake: "LensMake",  # ASCII, count any
                piexif.ExifIFD.Sharpness: 65535,  # SHORT, count 1 ... also be accepted '(65535,)'
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),  # Rational, count 4
                }
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
               piexif.GPSIFD.GPSAltitudeRef: 1,  # BYTE, count 1 ... also be accepted '(1,)'
               }
    exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    
    # round trip
    piexif.insert(exif_bytes, "foo.jpg")
    exif_dict_tripped = piexif.load("foo.jpg")

On GoogleAppEngine
------------------

Files cannot be saved to disk when using GoogleAppEngine. Therefore, files must be handled in memory.

::

    jpg_data = self.request.get("jpeg")
    output = io.BytesIO()

    # load
    exif = piexif.load(jpg_data)
    
    # insert
    piexif.insert(exif_bytes, jpg_data, output)

    # remove
    piexif.remove(jpg_data, output)

    # transplant
    piexif.transplant(jpg_data1, jpg_data2, output)

Invalid EXIF Thumbnails
-----------------------

EXIF data will sometimes be either corrupted or written by non-compliant software. When this happens, it's possible
that the thumbnail stored in EXIF cannot be found when attempting to dump the EXIF dictionary.

A good solution would be to remove the thumbnail from the EXIF dictionary and then re-attempt the dump:

::

    try:
        exif_bytes = piexif.dump(exif_dict)
    except InvalidImageDataError:
        del exif_dict["1st"]
        del exif_dict["thumbnail"]
        exif_bytes = piexif.dump(exif_dict)

