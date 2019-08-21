#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.auxiliary import http

NAME = 'Google'
URL = None

def googleSearch(query, page = 0, rpp = 10): # rpp = results per page, default 10
    urls = list()

    url = 'https://google.com/search?q=%s&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start=%s&filter=0' % (query, page * rpp)

    response = http.get(url).text

    if 'Our systems have detected unusual traffic' in response:
        return urls

    if 'did not match any documents' in response:
        return urls

    cases = response.split('<cite')[1:]

    for case in cases:
        result = case.split('>')[1].split('</cite')[0]

        if result.startswith('http'):
            urls.append(result)

    return urls

def scan(scanner, domain):
    subdomains = set()

    for i in range(10): # TODO: use verbosity passed by `scanner` object
        results = set(googleSearch('site:.?'.replace('?', domain), page = i))

        if len(results) == 0:
            break

        subdomains.update(results)

    return subdomains

