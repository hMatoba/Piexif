from ._remove import remove
from ._load_and_dump import load, dump, ImageGroup, PhotoGroup, GPSInfoGroup
from ._transplant import transplant
try:
    from ._thumbnail import thumbnail
except ImportError:
    print("'thumbnail' function depends on PIL or Pillow.")


VERSION = '0.1.2'