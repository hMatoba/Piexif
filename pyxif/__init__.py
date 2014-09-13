from remove import remove
from rwexif import load, load_from_file, dump
from transplant import transplant
try:
    from thumbnail import thumbnail
except ImportError:
    print("'thumbnail' function depends on PIL or Pillow.")