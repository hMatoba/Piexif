Pyxif
=====================

To simplify exif manipulations with python.


Functions
--------
    dump - converts dict to exif bytes
    load - converts exif bytes to dict
    load_from_file - loads exif from file, and converts to dict
    remove - removes exif from JPEG
    thumbnail - resizes proportionally without loosing exif(depend on PIL or Pillow)
    transplant - transplants exif to another JPEG


How to Use
--------
    # dump
    im = Image.open(input_file)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    zeroth_ifd = {282: (96, 1),
                  283: (96, 1),
                  296: 2,
                  305: 'paint.net 4.0.3'}
    exif_bytes = pyxif.dump(zeroth_ifd=zeroth_ifd)
    im.save(output_file, exif=exif_bytes)

    # load_from_file
    zeroth_dict, exif_dict, gps_dict = pyxif.load_from_file(input_file)

    # remove
    pyxif.remove("in.jpg", "out.jpg")

    # thumbnail
    pyxif.thumbnail("in.jpg", "out", (80, 80))

    # transplant
    pyxif.transplant("exif_src.jpg", "image.jpg", "out.jpg")


Depends on
--------
  Function "thumbnail" depends on PIL, or Pillow.
  Others don't depend on any 3rd module.


Environment
--------
  Python 2.7(partly checked on 3.4)