Piexif
======

|Build Status| |Windows Build| |Coverage Status| |docs|


This is a renamed project from Pyxif. To simplify exif manipulations with python. Writing, reading, and more... Piexif is pure python. To everywhere with Python.


Document: http://piexif.readthedocs.org/en/latest/

Online demo: http://piexif-demo.appspot.com/demo

Install
-------

'easy_install'::

    $ easy_install piexif

or 'pip'::

    $ pip install piexif

or download .zip, extract it. Put 'piexif' directory into your environment.

Why Choose Piexif
-----------------

- OS independent
- Pure Python. So, runs on Python 2.7, 3.3, 3.4, 3.5 and...
- Easy exif manipulations. Read, write, remove...
- Documented. http://piexif.readthedocs.org/en/latest/

How to Use
----------

There are only just five functions.

- *load(filename)* - Get exif data as *dict*.
- *dump(exif_dict)* - Get exif as *bytes* to save with JPEG.
- *insert(exif_bytes, filename)* - Insert exif into JPEG.
- *remove(filename)* - Remove exif from JPEG.
- *transplant(filename, filename)* - Transplant exif from JPEG to JPEG.

Example
-------

::

    exif_dict = piexif.load("foo1.jpg")
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

With PIL(Pillow)
----------------

::

    from PIL import Image
    import piexif

    im = Image.open(filename)
    exif_dict = piexif.load(im.info["exif"])
    # process im and exif_dict...
    w, h = im.size
    exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
    exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
    exif_bytes = piexif.dump(exif_dict)
    im.save(new_file, "jpeg", exif=exif_bytes)

Environment
-----------

Tested on Python 2.7, 3.3, 3.4, 3.5, pypy, and pypy3. Piexif would run even on IronPython. Piexif is OS independent and can run on GoogleAppEngine.

License
-------

This software is released under the MIT License, see LICENSE.txt.

.. |Build Status| image:: https://img.shields.io/travis/hMatoba/Piexif/master.svg?label=Linux%20build
   :target: https://travis-ci.org/hMatoba/Piexif
.. |Coverage Status| image:: https://coveralls.io/repos/hMatoba/Piexif/badge.svg?branch=master
   :target: https://coveralls.io/r/hMatoba/Piexif?branch=master
.. |docs| image:: https://readthedocs.org/projects/piexif/badge/?version=latest
   :target: https://readthedocs.org/projects/piexif/
.. |Windows Build| image:: https://img.shields.io/appveyor/ci/hmatoba/piexif.svg?label=Windows%20build
   :target: https://ci.appveyor.com/project/hMatoba/piexif