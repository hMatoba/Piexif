Piexif
======

|Build Status| |Coverage Status| |docs|

This is a renamed project from Pyxif. To simplify exif manipulations with python. Writing, reading, and more... Piexif is pure python. To everywhere with Python.

Document: http://piexif.readthedocs.org/en/1.0.x/

Install
-------

Download .zip, extract it and run

::

    $ python setup.py install

Example
-------

::

    exif_dict = piexif.load("foo1.jpg")
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            print(ifd, tag, exif_dict[ifd][tag])

Environment
-----------

Tested on Python 2.7, 3.3, 3.4, pypy, and pypy3. Piexif would run even on IronPython. Piexif is OS independent and can run on GoogleAppEngine.

License
-------

This software is released under the MIT License, see LICENSE.txt.

.. |Build Status| image:: https://travis-ci.org/hMatoba/Piexif.svg?branch=master
   :target: https://travis-ci.org/hMatoba/Piexif
.. |Coverage Status| image:: https://coveralls.io/repos/hMatoba/Piexif/badge.svg?branch=master
   :target: https://coveralls.io/r/hMatoba/Piexif?branch=master
.. |docs| image:: https://readthedocs.org/projects/piexif/badge/?version=latest
   :target: https://readthedocs.org/projects/piexif/
