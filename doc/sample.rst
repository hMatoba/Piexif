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

Example) rotate the image by its exif orientation tag value and remove the orientation tag from the image's exif data:

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
                    img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 7:
                    img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

                img.save(filename, exif=exif_bytes)

Piexif on Server
----------------

Piexif stores the image's exif data as a dictionary. This dictionary is easy to convert to JSON for use with AJAX or for use with document oriented databases.

::

    """GoogleAppEngine and Python 2.7"""
    import json
    
    import tornado.web
    import tornado.wsgi
    import piexif
    
    
    class PostHandler(tornado.web.RequestHandler):
        def post(self):
            jpg_data = self.request.body
            try:
                exif_dict = piexif.load(jpg_data)
            except:
                self.set_status(400)
                return self.write("Wrong jpeg")
            self.add_header("Content-Type", "application/json")
            thumbnail = exif_dict.pop("thumbnail")
            data_d = {}
            for ifd in exif_dict:
                data_d[ifd] = {piexif.TAGS[ifd][tag]["name"]:exif_dict[ifd][tag]
                               for tag in exif_dict[ifd]}
            data_d["thumbnail"] = thumbnail
            data = json.dumps(data_d, encoding="latin1")
            return self.write(data)
    
    application = tornado.web.Application([
        (r"/p", PostHandler),
    ])
    
    application = tornado.wsgi.WSGIAdapter(application)
