#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging

class UpperModule(Module):
    def execute(self, context):
        context.output = str(context.stdin).upper()
        return context

