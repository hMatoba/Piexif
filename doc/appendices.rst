==========
Appendices
==========

On GoogleAppEngine
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

Exif data as dict
-----------------
something here...

Tag Name and Value Type
-----------------------
| Each exif tag has appropriate type of the value. BYTE, ASCII, SHORT, or...
| See the document of Exif.
| http://www.kodak.com/global/plugins/acrobat/en/service/digCam/exifStandard2.pdf
| Some examples are shown below. If value type is number and count is two or more, use tuple.

::

    BYTE: {GPSIFD.GPSAltitudeRef: 1}
    ASCII: {ZerothIFD.Make: u"Make"}
    SHORT: {ZerothIFD.ResolutionUnit: 65535}
    SHORT(count:3): {ZerothIFD.BitsPerSample: (24, 24, 24)}
    LONG: {ZerothIFD.JPEGInterchangeFormatLength: 4294967295}
    RATIONAL: {ZerothIFD.XResolution: (4294967295, 1)}
    UNDEFINED: {ExifIFD.OECF: b"\xaa\xaa\xaa\xaa\xaa\xaa"}
    SRATIONAL(count:3): {ZerothIFD.BlackLevelDeltaH: ((1, 1), (1, 1), (1, 1))}
