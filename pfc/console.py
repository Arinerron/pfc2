#!/usr/bin/env python3

from pfc.core import Core
from pfc import tools, colors

#from curses import wrapper
import readline
import sys, logging

class Console:
    def __init__(self, window = None, core = None):
        self.running = True

        self.window = window
        self.core = (Core() if core is None else core)
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

        while self.running:
            try:
                line = self.read_line(colors.reset + colors.fg_green + colors.bold + 'pfc' + colors.reset + colors.bold + status_map.get(last_status, '-') + '> ' + colors.reset + colors.fg_cyan)
                
                sys.stdout.write(colors.reset)
                sys.stdout.flush()

                context = self.core.execute_command(self.core.parse_command(line))
                last_status = context.status
            except EOFError as e:
                self.running = False
                print()
                logging.info('Goodbye!')
            except KeyboardInterrupt:
                print()
                logging.info('Use ^D or "quit" to exit.')

    def stop(self):
        for module in self.core.modules:
            module['class'].stop()

if __name__ == '__main__':
    console = wrapper(Console)
