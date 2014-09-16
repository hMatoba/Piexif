Pyxif
=====================

To simplify exif manipulations with python.
Pyxif isn't a wrapper. To everywhere with Python(function'thumbnail' depends on PIL or Pillow).

Functions
--------
    dump - converts dict to exif bytes
    insert - inserts exif bytes to JPEG
    load - converts exif bytes to dict
    remove - removes exif from JPEG
    thumbnail - resizes proportionally without loosing exif(depend on PIL or Pillow)
    transplant - transplants exif to another JPEG


How to Use
--------
    # dump and insert
    zeroth_ifd = {pyxif.ImageGroup.Make: "Canon",
                  pyxif.ImageGroup.XResolution: (96, 1),
                  pyxif.ImageGroup.YResolution: (96, 1),
                  pyxif.ImageGroup.Software: "paint.net 4.0.3",
                  }
    exif_bytes = pyxif.dump(zeroth_ifd)
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


Depends on
--------
  Function "thumbnail" depends on PIL, or Pillow(Tested on Pillow 2.5.3).
  Others don't depend on any 3rd module.


Environment
--------
  Checked on Python 2.7, 3.3 and 3.4.


Note
--------
  'load' can't read little endian exif.


License
--------
  This software is released under the MIT License, see LICENSE.txt.