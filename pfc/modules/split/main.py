#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging

class SplitModule(Module):
    def execute(self, context):
        splitat = ' '

        if len(context.args) >= 1:
            splitat = context.args[0]

        context.output = context.stdin.split(splitat)

        return context

