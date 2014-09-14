Pyxif
=====================

To simplify exif manipulations with python.
Not a wrapper.

Functions
--------
    dump - converts dict to exif bytes
    load - converts exif bytes to dict
    remove - removes exif from JPEG
    thumbnail - resizes proportionally without loosing exif(depend on PIL or Pillow)
    transplant - transplants exif to another JPEG


How to Use
--------
    # dump
    im = Image.open("in.jpg")
    im.thumbnail((100, 100), Image.ANTIALIAS)
    zeroth_ifd = {282: (96, 1),
                  283: (96, 1),
                  296: 2,
                  305: 'paint.net 4.0.3'}
    exif_bytes = pyxif.dump(zeroth_ifd=zeroth_ifd)
    im.save(output_file, exif=exif_bytes)

    # load
    zeroth_dict, exif_dict, gps_dict = pyxif.load("in.jpg")

    # remove
    pyxif.remove("in.jpg")

    # thumbnail
    pyxif.thumbnail("in.jpg", "out.jpg", (80, 80))

    # transplant
    pyxif.transplant("exif_src.jpg", "image.jpg")


Depends on
--------
  Function "thumbnail" depends on PIL, or Pillow(Tested on Pillow 2.5.3).
  Others don't depend on any 3rd module.


Environment
--------
  Checked on Python 2.7 and 3.4


Note
--------
  Only for big endian files


License
--------
  This software is released under the MIT License, see LICENSE.txt.