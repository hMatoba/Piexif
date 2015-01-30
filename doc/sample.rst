=======
Samples
=======

Rotate Image by Exif Orientation
--------------------------------

Rotate image by exif orientation tag and remove orientation tag.

::

    from PIL import Image
    import piexif


    def rotate_jpeg(filename):
        zeroth_ifd, exif_ifd, gps_ifd = piexif.load(filename)

        if piexif.ZerothIFD.Orientation in zeroth_ifd:
            orientation = zeroth_ifd.pop(piexif.ZerothIFD.Orientation)
            exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)

            img = Image.open(filename)
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90)
            elif orientation == 7:
                img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90)

            img.save(filename, exif=exif_bytes)
