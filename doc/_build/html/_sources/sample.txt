=======
Samples
=======

Check Containing Tag
--------------------

::

    from PIL import Image
    import piexif


    exif = piexif.load(filename)
    if piexif.ImageIFD.Orientation in exif["0th"]:
        print("Orientation is ", exif["0th"][piexif.ImageIFD.Orientation])
    if piexif.ExifIFD.Gamma in exif["Exif"]:
        print("Gamma is ", exif["Exif"][piexif.ExifIFD.Gamma])

Rotate Image by Exif Orientation
--------------------------------

Rotate image by exif orientation tag and remove orientation tag.

::

    from PIL import Image
    import piexif


    def rotate_jpeg(filename):
        exif = piexif.load(filename)

        if piexif.ImageIFD.Orientation in exif["0th"]:
            orientation = exif["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif)

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
