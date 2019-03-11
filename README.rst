Piexif
======

|Build Status| |Windows Build| |Coverage Status| |docs|


To simplify exif manipulations with Python. Writing, reading, and more... Piexif is pure Python. To everywhere with Python.


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

- Pure Python. So, it runs everywhere where Python runs.
- Easy exif manipulations. Read, write, remove...
- Documented. http://piexif.readthedocs.org/en/latest/

How to Use
----------

There are only just five functions.

- *load(filename)* - Get exif data as *dict*.
- *dump(exif_dict)* - Get exif as *bytes*.
- *insert(exif_bytes, filename)* - Insert exif into JPEG, or WebP.
- *remove(filename)* - Remove exif from JPEG, or WebP.
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

Tested on Python 2.7, 3.5+ and PyPy3. Piexif would run even on IronPython. Piexif is OS independent and can run on Google App Engine.

License
-------

This software is released under the MIT license, see LICENSE.txt.

.. |Build Status| image:: https://api.travis-ci.org/hMatoba/Piexif.svg?branch=master
   :target: https://travis-ci.org/hMatoba/Piexif
.. |Windows Build| image:: https://ci.appveyor.com/api/projects/status/github/hMatoba/Piexif?branch=master&svg=true
   :target: https://ci.appveyor.com/project/hMatoba/piexif
.. |Coverage Status| image:: https://coveralls.io/repos/hMatoba/Piexif/badge.svg?branch=master
   :target: https://coveralls.io/r/hMatoba/Piexif?branch=master
.. |docs| image:: https://readthedocs.org/projects/piexif/badge/?version=latest
   :target: https://readthedocs.org/projects/piexif/
