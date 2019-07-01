Changelog
=========

1.1.3
-----

- Fix failure to decode a minimal 1 x 1 pixel JPEG. Related to https://github.com/hMatoba/Piexif/pull/93.

1.1.2
-----

- Resolve issue. https://github.com/hMatoba/Piexif/issues/64

1.1.1
-----

- Ignore XMP segment. Related to https://github.com/hMatoba/Piexif/pull/74.

1.1.0b
------

- "load", "insert", and "remove" support WebP format.

1.0.13
------

- Added helper function to read and write "UserComment".
- Added to support for SignedByte, SigendShort, Float, and Double.

1.0.12
------

- Added explicit InvalidImageDataError exception to aid users. Related to https://github.com/hMatoba/Piexif/issues/30.
- Fixed minor issue with tests.
- Removed minor amounts of unused logic.
- Updated .travis.yml for Python and Pillow versions.

1.0.11
------

- Add option argument to "load".

1.0.10
------

- Add tags in Exif ver.2.31

1.0.9
-----

- Performance up "load" jpeg from file.

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
