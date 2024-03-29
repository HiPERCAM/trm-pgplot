from setuptools import setup, Extension
import os, numpy, sys
from codecs import open
from os import path
from Cython.Build import cythonize

"""Setup script for the pgplot Cython wrapper"""

# setup the paths to get the libraries and headers
include_dirs = []
if "PGPLOT_PNG" in os.environ:
    if os.environ["PGPLOT_PNG"] == "true":
        libraries = ["cpgplot", "pgplot", "X11", "m", "gfortran", "png", "z"]
    elif os.environ["PGPLOT_PNG"] == "false":
        libraries = ["cpgplot", "pgplot", "X11", "m", "gfortran"]
    else:
        raise Exception('Environment variable PGPLOT_PNG neither "true" nor "false"')
else:
    raise Exception("Environment variable PGPLOT_PNG not defined")

library_dirs = ["/usr/X11R6/lib", "/opt/local/lib", "/opt/homebrew/lib"]
library_dirs = [d for d in library_dirs if os.path.exists(d)]

include_dirs.append(numpy.get_include())

if os.name == "posix":
    if "PGPLOT_DIR" in os.environ:
        library_dirs.append(os.environ["PGPLOT_DIR"])
        include_dirs.append(os.environ["PGPLOT_DIR"])
    else:
        raise Exception("Environment variable PGPLOT_DIR not defined!")
else:
    raise Exception("os = {:s} not supported".format(os.name))

pgplot = [
    Extension(
        "trm.pgplot._pgplot",
        [os.path.join("trm", "pgplot", "_pgplot.pyx")],
        libraries=libraries,
        library_dirs=library_dirs,
        include_dirs=include_dirs,
        extra_compile_args=[],
        define_macros=[("MAJOR_VERSION", "0"), ("MINOR_VERSION", "1")],
    ),
]

setup(
    name="trm.pgplot",
    version="0.93",
    packages=[
        "trm",
        "trm.pgplot",
    ],
    ext_modules=cythonize(pgplot, include_path=["trm/pgplot"]),
    zip_safe=False,
    # metadata
    author="Tom Marsh",
    author_email="t.r.marsh@warwick.ac.uk",
    description="Python/Cython wrapper of pgplot",
    url="http://www.astro.warwick.ac.uk/",
)
