from setuptools import setup

import pyxif

setup(
    name = "Pyxif",
    version = pyxif.VERSION,
    author = "hMatoba",
    author_email = "hiroaki.mtb@outlook.com",
    description = ("Exif manipulation tool(writing, reading, and more...) in Python."),
    license = "MIT",
    keywords = ["exif", "jpeg"],
    url = "https://github.com/hMatoba/Pyxif",
    packages = ['pyxif'],
    data_files = [("", ["LICENSE.txt"])],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia",
    ]
)