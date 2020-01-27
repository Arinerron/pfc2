#!/usr/bin/env python3

from pfc.core import Core
from pfc import tools, colors

#from curses import wrapper
import readline
import sys
from pfc import logger

class PFCCompleter:
    def __init__(self, core):
        self.core = core

    def complete(self, text, state):
        output = None

        if state == 0:
            if text:
                self.matches = [ s for s in list(self.core.modules.keys()) if s and s.startswith(text) ]
            else:
                self.matches = list(self.core.modules.keys())[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response

class Console:
    def __init__(self, window = None, core = None):
        self.running = True

        self.window = window
        self.core = (Core() if core is None else core)

        # tab completion
        self.completer = PFCCompleter(self.core)
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind('tab: complete')

        # start console
        self.start()
        self.execute()

    def start(self):
        for name, module in self.core.modules.items():
            if not 'class_instance' in module:
                module['class_instance'] = module['class'](self.core, name)
            module['class_instance'].start()

        # TODO: Add one of those cool header thingies with random quotes like radare2

    def read_line(self, prompt = ''):
        return input(prompt)

        # TODO: clean this up
        build = ''

        max_height, max_width = self.window.getmaxyx()

        while self.running:
            y, x = self.window.getyx()
            char = self.window.getkey()

            if not char == 'KEY_UP':
                build += char

            self.window.addstr(max_height - 1, 0, build)
            self.window.refresh()

    def execute(self):
        last_status = -1

        status_map = {
            -1 : '=',
            0 : '+',
            1 : '='
        }

        running_something = False # this is used for the ^D message

        while self.running:
            try:
                running_something = False

                line = self.read_line(colors.reset + colors.fg_green + colors.bold + 'pfc' + colors.reset + colors.bold + status_map.get(last_status, '-') + '> ' + colors.reset + colors.fg_cyan)

                sys.stdout.write(colors.reset)
                sys.stdout.flush()

                running_something = True

                context = self.core.execute_command(self.core.parse_command(line))

                running_something = False

                last_status = context.status
            except EOFError as e:
                self.running = False
                print()
                logger.info('Goodbye!')
            except KeyboardInterrupt:
                print()

                if not running_something:
                    logger.info('Use ^D or "quit" to exit.')

    def stop(self):
        for module in self.core.modules:
            module['class'].stop()

if __name__ == '__main__':
    console = wrapper(Console)
