# -*- coding: utf-8 -*-

"""Top-level package for SarcomereAnnotation."""

__author__ = 'Jamie Sherman'
__email__ = 'jamies@alleninstitute.org'
__version__ = '0.1.0'


def get_module_version():
    return __version__


from .SarcomereLines import SarcomereLines
from .Picture import Picture
