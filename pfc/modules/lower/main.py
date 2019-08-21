#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging

class LowerModule(Module):
    def execute(self, context):
        context.output = str(context.stdin).lower()
        return context

