#!/usr/bin/env python3

from pfc import module, tools, colors

import subprocess, os
from pfc import logger

class Core:
    def __init__(self):
        self.modules = module.import_all_modules(self, tools.get_dir() + '/modules')
        self.commands = {}

        for module_name, module_obj in self.modules.items():
            self.commands[module_name] = module_obj

            for name in module_obj['aliases']:
                self.commands[name] = module_obj

    def register_command(self, name, command):
        if not 'class_instance' in command:
            command['class_instance'] = command.get('class')(self, command.get('name', name))

        self.commands[name] = commands

        return self

    def execute_command(self, command, stdin = None, strict = False):
        cmd = command.get('command')
        pipe = command.get('output')
        args = command.get('arguments', [])

        context = module.Context(stdin, args)
        context.core = self

        command_exists = command.get('command', None) in self.commands

        if cmd in [None, '']:
            context.status = module.NA
            return context
        elif cmd.startswith('!') and not strict:
            # execute interactively

            context.status = os.system(command['unparsed'].replace('!', '', 1)) # remove first !
            context.output = None

            # XXX: remove duplicate code
            if not pipe is None:
                context = self.execute_command(pipe, stdin = context.output)

            return context
        elif not command_exists and not strict:
            # XXX: refactor and have a list of functions to call from
            # try to execute a shell command
            try:
                process = subprocess.Popen([cmd] + args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)

                stdin = self.execute_command({
                    'command': 'cat',
                    'output' : None
                }, stdin = stdin, strict = True).output

                # XXX: figure out what the default `input` should be if `stdin` is `None`
                if not stdin in [None, 'None']:
                    stdout, stderr = process.communicate(input = str(stdin).encode())
                else:
                    stdout, stderr = process.communicate()

                status = process.wait()

                if len(stderr) != 0:
                    for line in stderr.strip().split(b'\n'):
                        logger.error(line.decode('utf-8'))

                context.status = status
                context.output = (None if len(stdout) == 0 else stdout.decode('utf-8'))

                # XXX: remove duplicate code
                if not pipe is None:
                    context = self.execute_command(pipe, stdin = context.output)

                return context
            except FileNotFoundError:
                # if it's not found, try the next "method"
                pass

        if not command_exists:
            context.status = module.NOT_FOUND
            logger.warn('Command not found: ' + colors.reset + '%s' % command.get('command', '<none>'))
            return context

        command = self.commands[cmd]

        context.args = command['parser'].parse(args)

        instance = command['class_instance']
        instance.execute(context)

        if not pipe is None:
            context = self.execute_command(pipe, stdin = context.output)

        return context

    def parse_command(self, line):
        in_string = False
        pipe = False
        escaped = False

        # this is so that the buffer at the end is added to build
        line += ' '

        build = {
            'unparsed' : line,
            'arguments' : [],
            'output' : {
                'command' : 'cat',
                'arguments' : ['--stdout', '--newline']
            }
        }

        temp = None
        str_temp = ''

        normal_map = {
            'n' : '\n',
            'r' : '\r',
            "'" : "'",
            "\\" : "\\"
        }

        # TODO: add normal_map copy but for single quotes.

        str_map = {
            "'" : "'",
            "\\" : "\\"
        }

        for char in line:
            if pipe:
                temp += char
            elif in_string:
                if char == "'" and not escaped:
                    in_string = False
                    build['arguments'].append(str_temp)
                    str_temp = ''
                    escaped = False
                elif char == "\\" and not escaped:
                    escaped = True
                else:
                    str_temp += (str_map.get(char, "\\" + char) if escaped else char)
                    escaped = False
            else:
                if char == ' ' and (not escaped):
                    if not temp is None:
                        build['arguments'].append(temp)
                        temp = None
                    continue

                if char == "'" and not escaped:
                    in_string = True

                    if not temp is None:
                        build['arguments'].append(temp)
                        temp = None

                    continue

                if char == '|' and not escaped:
                    if not temp is None:
                        build['arguments'].append(temp)
                    pipe = True
                    temp = ''
                    continue

                if temp is None:
                    temp = ''

                if char == '\\' and not escaped:
                    escaped = True
                    continue
                else:
                    temp += (normal_map.get(char, "\\" + char) if escaped else char)

                escaped = False

        if pipe:
            build['output'] = self.parse_command(temp)

        if len(build['arguments']) != 0:
            build['command'] = build['arguments'].pop(0)

        return build
