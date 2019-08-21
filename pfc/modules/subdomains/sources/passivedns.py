#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.auxiliary import http

NAME = 'PassiveDNS'
URL = 'http://ptrarchive.com/tools/search3.htm?label=%s'

def scan(scanner, domain):
    urls = set()

    for case in http.get(URL % domain).text:
        case = case.split(' ')[0]

        if (domain in case) and (not '@' in case) and (not '/' in case) and (not ':' in case):
            urls.add(case)

    return urls

