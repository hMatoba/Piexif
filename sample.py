import os

import piexif
from PIL import Image


def load_sample(input_file):
    exif = piexif.load(input_file)
    thumbnail = exif.pop("thumbnail")
    if thumbnail is not None:
        with open("foo.jpg", "wb+") as f:
            f.write(thumbnail)
    for ifd_name in exif:
        print("\n{0} IFD:".format(ifd_name))
        for key in exif[ifd_name]:
            try:
                print(key, exif[ifd_name][key][:10])
            except:
                print(key, exif[ifd_name][key])


def dump_sample(input_file, output_file):
    zeroth_ifd = {piexif.ImageIFD.Make: "foo",
                  piexif.ImageIFD.XResolution: (96, 1),
                  piexif.ImageIFD.YResolution: (96, 1),
                  piexif.ImageIFD.Software: "pixief",
                  }

    exif_bytes = piexif.dump({"0th":zeroth_ifd})
    im = Image.open(input_file)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)


def remove_sample():
    piexif.remove(os.path.join("tests", "images", "01.jpg"),
                 "remove_sample.jpg")


def transplant_sample():
    piexif.transplant(os.path.join("tests", "images", "01.jpg"),
                     os.path.join("tests", "images", "02.jpg"),
                     "transplant_sample.jpg")


def insert_sample():
    zeroth_ifd = {282: (96, 1),
                  283: (96, 1),
                  296: 2,
                  305: 'piexif'}
    exif_bytes = piexif.dump({"0th":zeroth_ifd})
    piexif.insert(exif_bytes,
                 "remove_sample.jpg",
                 "insert_sample.jpg")


if __name__ == "__main__":
    load_sample(os.path.join("tests", "images", "01.jpg"))
    dump_sample(os.path.join("tests", "images", "01.jpg"), "dump_sample.jpg")
    remove_sample()
    transplant_sample()
    insert_sample()
