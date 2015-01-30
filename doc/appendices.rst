==========
Appendices
==========

Exif Data in Piexif
-------------------

Each exif tag has appropriate type of the value. BYTE, ASCII, SHORT, or... See the document of Exif.
http://www.kodak.com/global/plugins/acrobat/en/service/digCam/exifStandard2.pdf

+---------------+----------------------+
| **Exif Type** | **Python Type(3.x)** |
+---------------+----------------------+
| BYTE          | int                  |
+---------------+----------------------+
| ASCII         | str                  |
+---------------+----------------------+
| SHORT         | int                  |
+---------------+----------------------+
| LONG          | int                  |
+---------------+----------------------+
| RATIONAL      | (int, int)           |
+---------------+----------------------+
| UNDEFINED     | bytes                |
+---------------+----------------------+
| SRATIONAL     | (int, int)           |
+---------------+----------------------+

If value type is number(BYTE, SHORT, LONG, RATIONAL, or SRATIONAL) and value count is two or more number, it is expressed with tuple.

+---------------------+-------------------------------+
| BYTE, SHORT, LONG   | (int, int, ...)               |
+---------------------+-------------------------------+
| RATIONAL, SRATIONAL | ((int, int), (int, int), ...) |
+---------------------+-------------------------------+

Exif in piexif example is below.

::

    zeroth_ifd = {piexif.ZerothIFD.Make: u"Canon",  # ASCII, count any
                  piexif.ZerothIFD.XResolution: (96, 1),  # RATIONAL, count 1
                  piexif.ZerothIFD.YResolution: (96, 1),  # RATIONAL, count 1
                  piexif.ZerothIFD.Software: u"piexif"  # ASCII, count any
                  }
    exif_ifd = {piexif.ExifIFD.ExifVersion: b"\x02\x00\x00\x00"  # UNDEFINED, count 4
                piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",  # ASCII, count 20
                piexif.ExifIFD.LensMake: u"LensMake",  # ASCII, count any
                piexif.ExifIFD.Sharpness: 65535,  # SHORT, count 1
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),  # Rational, count 4
                }
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
               piexif.GPSIFD.GPSAltitudeRef: 1,  # BYTE, count 1
               }
    exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    
    # round trip
    piexif.insert(exif_bytes, "foo.jpg")
    z, e, g = piexif.load("foo.jpg")

On GoogleAppEngine
------------------

On GoogleAppEngine, it can't save files on disk. Therefore files must be handled on memory.

::

    jpg_data = self.request.get("jpeg")
    output = io.BytesIO()

    # load
    zeroth_dict, exif_dict, gps_dict = piexif.load(jpg_data)
    
    # insert
    piexif.insert(exif_bytes, jpg_data, output)

    # remove
    piexif.remove(jpg_data, output)

    # transplant
    piexif.transplant(jpg_data1, jpg_data2, output)
