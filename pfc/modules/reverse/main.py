#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

from pfc import logger

class ReverseModule(Module):
    def execute(self, context):
        output = ''

        if isinstance(context.stdin, list) or isinstance(context.stdin, set):
            output = type(context.stdin)(reversed(context.stdin))
        else:
            output = ''.join(reversed(context.stdin))

        context.output = output
        
        return context

