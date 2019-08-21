#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

import pkgutil

__all__ = ['ask', 'crtsh', 'google', 'passivedns', 'threatcrowd']

# https://stackoverflow.com/a/3365846/3678023
__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()

blacklist = ['is_pkg', 'loader', 'module_name', 'pkgutil', 'blacklist', 'sources']
sources = []

from . import ask, crtsh, google, passivedns, threatcrowd

for source in dir():
    if (not source.startswith('_')) and not source in blacklist:
        sources.append(eval(source))
