from ._remove import remove
from ._load_and_dump import load, dump, ZerothIFD, ExifIFD, GPSIFD
from ._transplant import transplant
from ._insert import insert
try:
    from ._thumbnail import thumbnail
except ImportError:
    print("'thumbnail' function depends on PIL or Pillow.")


VERSION = '0.5.0'