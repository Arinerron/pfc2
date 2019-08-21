#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.auxiliary import http

NAME = 'crt.sh'
URL = 'https://crt.sh/?q=%%25%s'

def scan(scanner, domain):
    urls = set()

    for case in http.get(URL % domain).text.split('<TD>')[1:]:
        if not '<A ' in case:
            urls.add(case.split('</TD>')[0])

    return urls
