"""
independent chemical symbols
"""


__version__ = '1.0.0'

import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))

from atomtools.atomtools import *

def version():
    return __version__

