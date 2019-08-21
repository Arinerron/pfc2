#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging

class ModulesModule(Module):
    def execute(self, context):
        parameters = context.args

        update = parameters.get('update', [])
        install = parameters.get('install', [])
        remove = parameters.get('remove', [])

        if len(update) != 0:
            logging.info('Installing modules...')

        for module in update:
            tools.update(module)

        for module in install:
            tools.install(module)

        context.status = 0
        return context

