from setuptools import setup
import sys

import piexif


sys.path.append('./piexif')
sys.path.append('./tests')

with open("README.rst", "r") as f:
    description = f.read()

setup(
    name = "piexif",
    version = piexif.VERSION,
    author = "hMatoba",
    author_email = "hiroaki.mtb@outlook.com",
    description = "To simplify exif manipulations with python. " +
                  "Writing, reading, and more...",
    long_description = description,
    license = "MIT",
    keywords = ["exif", "jpeg"],
    url = "https://github.com/hMatoba/Piexif",
    packages = ['piexif'],
    test_suite = 's_test.suite',
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia",
        "Topic :: Printing",
    ]
)