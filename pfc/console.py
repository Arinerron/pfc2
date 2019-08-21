#!/usr/bin/env python3

from pfc.core import Core
from pfc import tools

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
                line = self.read_line('pfc' + status_map.get(last_status, '-') + '> ')
                context = self.core.execute_command(self.core.parse_command(line))
                last_status = context.status

                #if not context.output is None:
                #    print(context.output)
            except (KeyboardInterrupt, EOFError) as e:
                logging.info('Goodbye!')
                exit(1)


    def stop(self):
        for module in self.core.modules:
            module['class'].stop()

if __name__ == '__main__':
    console = wrapper(Console)
