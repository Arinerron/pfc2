#!/usr/bin/env python3

from pfc import console, core, tools

import shutil, os


template_script = '''#!/bin/sh

cd ../..

./main-modules.py "$@"
'''


bin_dir = tools.get_dir() + '/.pfc-bin/'

if __name__ == '__main__':
    core = core.Core()
    print(core.modules)

    try:
        shutil.rmtree
    except FileNotFoundError:
        pass

    os.mkdir(bin_dir)

    for name, module in core.modules.items():
        files = [module.get('name', [])] + module.get('aliases', [])

        for file in files:
            print(file)
