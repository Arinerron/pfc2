#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

import pkgutil

# https://stackoverflow.com/a/3365846/3678023
__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()
