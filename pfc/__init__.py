#!/usr/bin/env python3

__all__ = ['core', 'module', 'console', 'modules']

from pfc.module import *
from pfc import colors

class PFCFormatter(logging.Formatter):
    def __init__(self, fmt = colors.reset + colors.fg_green + colors.bold + '%(levelname)s: ' + colors.reset + colors.fg_green + '%(message)s' + colors.reset):
        self._default_fmt = fmt
        super().__init__(self, fmt)

    def format(self, message):
        level = message.levelno

        settings = {
            'default' : {
                'prefix' : ' ',
                'color' : '',
                'reset' : colors.reset
            },

            logging.DEBUG : {
                'prefix' : '/'
            },

            logging.INFO : {
                'prefix' : '*',
                'color' : colors.fg_green
            },

            logging.WARN : {
                'prefix' : '!',
                'color' : colors.fg_orange
            },

            logging.ERROR : {
                'prefix' : '-',
                'color' : colors.fg_red
            },

            logging.FATAL : {
                'prefix' : '-',
                'color' : colors.bg_red,
                'reset' : colors.bg_red
            }
        }

        default = settings['default']
        setting = settings.get(level, default)

        get = lambda s : setting.get(s, default[s])

        self._style._fmt = get('reset') + '[' + get('color') + get('prefix') + get('reset') + ']' + get('reset') + ' ' + get('color') + '%(message)s' + colors.reset

        output = logging.Formatter.format(self, message)

        self._style._fmt = self._default_fmt

        return output

import logging

formatter = PFCFormatter()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)

del handler, formatter, PFCFormatter
