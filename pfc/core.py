#!/usr/bin/env python3

from pfc import module, tools

import logging

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

    def execute_command(self, command, stdin = None):
        cmd = command.get('command')
        pipe = command.get('output')
        args = command.get('arguments', [])

        context = module.Context(stdin, args)

        if command.get('command', None) in [None, '']:
            context.status = module.NA
            return context
        elif not command.get('command', None) in self.commands:
            context.status = module.NOT_FOUND
            logging.warn('Command not found: %s' % command.get('command', '<none>'))
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
            'arguments' : [],
            'output' : {
                'command' : 'cat',
                'arguments' : ['--stdout']
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

