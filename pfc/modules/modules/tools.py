#!/usr/bin/env python3

def gitPull(repository):
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd = repository)
    return p.wait()

def gitClone(directory, repository):
    cmd = ['git', 'clone', repository]
    p = subprocess.Popen(cmd, cwd = directory)
    p.wait()
