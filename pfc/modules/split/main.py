#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging

class SplitModule(Module):
    def execute(self, context):
        # print(context.args) # TODO: Remove debug info and fix BUG: with splitting on delimiter ' '
        data = context.args['data']

        context.output = list()

        for d in data:
            if d == '-':
                d = context.stdin

            context.output.extend(d.split(context.args['delimiter'], context.args['count']))

        context.status = SUCCESS

        return context

