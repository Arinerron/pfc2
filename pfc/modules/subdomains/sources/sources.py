#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

class SubdomainSource:
    def __init__(self, root):
        self.root = root

    def get_name(self):
        return 'Template'

    def scan(self):
        return set()
    
