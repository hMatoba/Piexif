Changelog
=========

1.0.8
-----

- Exclude checking extension in "load".

1.0.7
-----

- Fix packaging.

1.0.6
-----

- Refactoring.

1.0.5
-----

- Bug fix: https://github.com/hMatoba/Piexif/issues/16

1.0.4
-----

- Fix APP1 matter.

1.0.3
-----

- Support SLong type.

1.0.2
-----

- Add some error detail to 'dump'.

1.0.1
-----

- Fix bug. 'load' and 'dump' InteroperabilityIFD was wrong.

1.0.0
-----

- Add handling InteroperabilityIFD, 1stIFD, and thumbnail image.
- *'load'* returns a dict that contains "0th", "Exif", "GPS", "Interop", "1st", and "thumbnail" keys.
- *'dump'* argument is changed from three dicts to a dict.
- *piexif.ZerothIFD* is renamed *piexif.ImageIFD* for 1stIFD support.

0.7.0c
------

- Rename project.
