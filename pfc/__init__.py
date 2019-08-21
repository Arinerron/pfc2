#!/usr/bin/env python3

__all__ = ['core', 'module', 'console', 'modules']

from pfc.module import *
from pfc import colors

import logging
logging.basicConfig(level = logging.INFO, format = colors.reset + colors.fg_green + colors.bold + '%(levelname)s: ' + colors.reset + colors.fg_green + '%(message)s' + colors.reset)

del colors
