import os

import piexif
from PIL import Image


def dump_sample(input_file, output_file):
    zeroth_ifd = {piexif.ImageIFD.Make: "fooooooooooooo",
                  piexif.ImageIFD.XResolution: (96, 1),
                  piexif.ImageIFD.YResolution: (96, 1),
                  piexif.ImageIFD.Software: "paint.net 4.0.3",
                  }

    exif_ifd = {piexif.ExifIFD.ExifVersion: b"0111",
                piexif.ExifIFD.Flash: (1,),
                piexif.ExifIFD.DateTimeOriginal: "1999:09:99 99:99:99",
                piexif.ExifIFD.CameraOwnerName: "Mr. John Doe",
                }

    gps_ifd = {piexif.GPSIFD.GPSAltitudeRef: 1,
               piexif.GPSIFD.GPSDateStamp: "1999:99:99",
               piexif.GPSIFD.GPSDifferential: 90,
               }

    exif = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd}
    exif_bytes = piexif.dump(exif)

    im = Image.open(input_file)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)


if __name__ == "__main__":
    dump_sample(os.path.join("tests", "images", "01.jpg"), "dump_sample.jpg")