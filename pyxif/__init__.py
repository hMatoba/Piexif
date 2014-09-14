from .remove import remove
from ._load_and_dump import load, dump, ImageGroup, PhotoGroup, GPSInfoGroup
from .transplant import transplant
try:
    from .thumbnail import thumbnail
except ImportError:
    print("'thumbnail' function depends on PIL or Pillow.")


VERSION = '0.1'