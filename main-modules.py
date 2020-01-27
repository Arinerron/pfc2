#!/usr/bin/env python3

import sys, os

sys.argv.pop(0) # this current file

# build context blob
context = {
    'name' : sys.argv.pop(0), # the command name
    'args' : sys.argv,
    'env' : dict(os.environ)
}

host = os.environ.get('PFC2_HOST', '127.0.0.1')
port = os.environ.get('PFC2_PORT')

if not port:
    sys.stderr.write('No PFC2_PORT specified. Did you accidentally clear your environmental variables?\n')
    exit(1)

import socket

# read forever from stdin until closed
# send to socket server on pfc
# pfc server determines if the stdin contains a unique id containing to a "context object" (which passes stdin/stdout/stderr or whatever)
# if so, get that data and pass that as stdin/stdout/stderr
# if not, just pass whatever to stdin
# pfc server sends back input over socket to the main-modules.py with instructions for what to write to stdin/stdout

# store the unique ids and objects forever so that you can store them in variables in bash
# add a feature to the fake `cat` module to convert from a pfc context object to raw data/str
