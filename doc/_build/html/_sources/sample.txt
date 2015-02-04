=======
Samples
=======

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

Check Containing Tag
--------------------

::

    from PIL import Image
    import piexif

    exif_dict = piexif.load(filename)
    if piexif.ImageIFD.Orientation in exif_dict["0th"]:
        print("Orientation is ", exif_dict["0th"][piexif.ImageIFD.Orientation])
    if piexif.ExifIFD.Gamma in exif_dict["Exif"]:
        print("Gamma is ", exif_dict["Exif"][piexif.ExifIFD.Gamma])

Rotate Image by Exif Orientation
--------------------------------

Rotate image by exif orientation tag and remove orientation tag.

::

    from PIL import Image
    import piexif

    def rotate_jpeg(filename):
        img = Image.open(filename)
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])

            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                exif_bytes = piexif.dump(exif_dict)

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
