#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

from pfc import logger
import sys

class CatModule(Module):
    def execute(self, context):
        args = context.args

        for src in args.get('file', ['-']):
            content = ''

            if src == '-':
                content = context.stdin

                if isinstance(content, list) or isinstance(content, set):
                    content = '\n'.join(content)
                elif content is None:
                    # XXX: refactor so this isn't duplicated code
                    context.success = SUCCESS
                    return context
                elif content is None and False: # TODO: fix BUG: here
                    build = list()

                    try:
                        while True:
                            build.append(input())
                    except KeyboardInterrupt:
                        content = '\n'.join(build)
            else:
                try:
                    with open(src, 'r') as f:
                        content = f.read()
                except FileNotFoundError as e:
                    logger.error('File not found: %s' % src)
                    context.status = FAILURE
                    continue
                except PermissionError as e:
                    logger.error('Permission denied: %s' % src)
                    context.status = FAILURE
                    continue

            content = str(content)

            if args.get('newline') and not content.endswith('\n'):
                content += '\n'

            if args.get('stdout'):
                sys.stdout.write(content)
                sys.stdout.flush()

            if args.get('stderr'):
                sys.stderr.write(content)
                sys.stderr.flush()

            if args.get('output'):
                if not context.output:
                    context.output = ''

                context.output += content

            if context.status != FAILURE:
                context.status = SUCCESS

        return context
