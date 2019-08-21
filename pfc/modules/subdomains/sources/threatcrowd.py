#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.auxiliary import http

NAME = 'Threatcrowd'
URL = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%s'

def scan(scanner, domain):
    urls = set()

    for case in http.get(URL % domain).text.split('"'):
        if (domain in case) and (not '@' in case) and (not '/' in case) and (not ':' in case):
            urls.add(case)

    return urls
