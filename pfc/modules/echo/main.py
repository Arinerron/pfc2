#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

from pfc import logger

class EchoModule(Module):
    def execute(self, context):
        context.output = ' '.join(context.args.get('content', [])) + ('' if context.args.get('no-newline', False) else '\n')

        return context
