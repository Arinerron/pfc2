#!/usr/bin/env python3

import os, sys

'''
get the location of the module in `module`
'''
def get_dir(module = None):
    if module is None:
        module = __file__
    else:
        module = module.__file__

    return os.path.dirname(os.path.realpath(module))

'''
wait until a single key is pressed
https://stackoverflow.com/a/34956791/3678023
'''
def wait_key():
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

'''
move the terminal cursor by the offset
'''
def move(curses, offset):
	y,x = curses.getyx()
	curses.move(y,x - offset)

