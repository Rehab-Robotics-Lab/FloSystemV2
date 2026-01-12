# flo_core/setup.py  –  keep it minimal
from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    version='0.1.0',           # must match <version> in package.xml
    packages=['flo_core'],
    package_dir={'': 'src'},
)

setup(**d)
