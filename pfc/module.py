#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc import tools, argparser

import sys, os, yaml, importlib.util
from pfc import logger

NA = -1
SUCCESS = 0
FAILURE = 1
NOT_FOUND = 2

def import_module(code, name, directory):
    main_file = code.get('main', 'main.py')
    class_name = 'Module'

    # path/to/module.py:ClassName
    if ':' in main_file:
        main_file2, class_name2 = tuple(main_file.split(':', 1))

        if len(main_file2.strip()) != 0:
            main_file = main_file2
        else:
            main_file = 'main.py'

        if len(class_name2.strip()) != 0:
            class_name = class_name2
        else:
            main_file = 'Module'

    # import the module from the file
    spec = importlib.util.spec_from_file_location('pfc.modules.%s' % name, directory + '/' + main_file)
    module = importlib.util.module_from_spec(spec)

    # add it to the path equivalent
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    # get the main class
    module_class = getattr(module, class_name)

    # return the dict object
    return {
        'name' : name,
        'aliases' : code.get('aliases', []),
        'code' : code,
        'module' : module,
        'parser' : argparser.ArgumentParser(code.get('parameters', {})),
        'class' : module_class,
        'config' : code
    }

def import_all_modules(core, modules_directory, import_modules = None):
    modules = dict()

    if not os.path.isdir(modules_directory):
        logger.fatal('Modules directory %s does not exist.' % modules_directory)
        return modules

    for directory in os.listdir(modules_directory):
        try:
            # if a set of modules is specified to import, only import those
            if not ((import_modules is None) or (not directory in import_modules)):
                continue

            module_yml = ''

            # two required files
            if 'module.yml' in os.listdir(modules_directory + '/' + directory):
                with open(modules_directory + '/' + directory + '/module.yml', 'r') as f:
                    module_yml = yaml.safe_load(f.read())

                # import the module and store it in the dict
                modules[module_yml.get('name', directory)] = import_module(module_yml, module_yml.get('name', directory), modules_directory + '/' + directory)
        except Exception as e:
            logger.fatal('Failed to import module %s.' % directory, exc_info = True)

    return modules

class Context:
    def __init__(self, stdin = None, args = None):
        self.status = NOT_FOUND
        self.stdin = stdin
        self.args_raw = args
        self.args = {}
        self.output = None

class Module:
    def __init__(self, core, name):
        self.core = core

        self.name = name
        self.aliases = []
        self.type = 'misc'
        self.description = None

        self.start()

    def start(self):
        return True

    def stop(self):
        return True

    def execute(self, context, parameters):
        context.status = NOT_FOUND
        return context
