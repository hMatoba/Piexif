from setuptools import setup
import sys

import pyxif


sys.path.append('./pyxif')
sys.path.append('./tests')

with open("README.rst", "r") as f:
    description = f.read()

setup(
    name = "Pyxif",
    version = pyxif.VERSION,
    author = "hMatoba",
    author_email = "hiroaki.mtb@outlook.com",
    description = description,
    license = "MIT",
    keywords = ["exif", "jpeg"],
    url = "https://github.com/hMatoba/Pyxif",
    packages = ['pyxif'],
    test_suite = 's_test.suite',
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia",
    ]
)