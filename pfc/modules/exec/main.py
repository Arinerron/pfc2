#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

from pfc import logger
import sys

class ExecModule(Module):
    def execute(self, context):
        command = ' '.join(context.args['data'])

        if command == '-':
            command = context.stdin

        try:
            context.output = eval(command)
            context.status = SUCCESS
        except Exception as e:
            logger.error('Failed to evaluate command', exc_info = True)
            context.status = FAILURE

        return context
