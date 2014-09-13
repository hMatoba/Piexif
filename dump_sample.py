import pyxif
from PIL import Image


def dump_sample(input_file, output_file):
    zeroth_ifd = {pyxif.ImageGroup.Make: "fooooooooooooo",
                  pyxif.ImageGroup.XResolution: (96, 1),
                  pyxif.ImageGroup.YResolution: (96, 1),
                  pyxif.ImageGroup.Software: "paint.net 4.0.3",
                  }

    exif_ifd = {pyxif.PhotoGroup.ExifVersion: "0111",
                pyxif.PhotoGroup.DateTimeOriginal: "1999:09:99 99:99:99",
                pyxif.PhotoGroup.CameraOwnerName: "Mr. John Doe",
                }

    gps_ifd = {pyxif.GPSInfoGroup.GPSDateStamp: "1999:99:99",
               pyxif.GPSInfoGroup.GPSDifferential: 90,
               }
    exif_bytes = pyxif.dump(zeroth_ifd=zeroth_ifd, exif_ifd=exif_ifd, gps_ifd=gps_ifd)

    im = Image.open(input_file)
    im.thumbnail((100, 100), Image.ANTIALIAS)
    im.save(output_file, exif=exif_bytes)

    z, e, g = pyxif.load(output_file)
    print(z, e, g)


if __name__ == "__main__":
    dump_sample(r"samples\01.jpg", r"samples\dump_sample.jpg")
