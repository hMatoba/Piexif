================
Helper Functions
================

UserComment
-----------
.. py:function:: piexif.helper.UserComment.load(data)

   Convert "UserComment" value in exif format to str.

   :param bytes data: "UserComment" value from exif
   :return: u"foobar"
   :rtype: str(Unicode)

::

    import piexif
    import piexif.helper
    exif_dict = piexif.load("foo.jpg")
    user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])

.. py:function:: piexif.helper.UserComment.dump(data, encoding="ascii")

   Convert str to appropriate format for "UserComment".

   :param data: Like u"foobar"
   :param str encoding: "ascii", "jis", or "unicode"
   :return: b"ASCII\x00\x00\x00foobar"
   :rtype: bytes

::

    import piexif
    import piexif.helper
    user_comment = piexif.helper.UserComment.dump(u"Edit now.")
    exif_dict = piexif.load("foo.jpg")
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
    exif_bytes = piexif.dump(exif_dict)
