#!/usr/bin/env python3
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['shape_completion_visualization'],
    package_dir={'': 'src'}
)
setup(**d)
