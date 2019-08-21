#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.auxiliary import http

NAME = 'Ask'
URL = None

def askSearch(query, page = 0):
    urls = list()

    url = 'http://www.ask.com/web?q=%s&page=%s' % (query, page)

    response = http.get(url).text

    if 'Make sure all words are spelled correctly' in response:
        return urls

    cases = response.split('<div class="PartialSearchResults-item-title">')[1:]

    for case in cases:
        try:
            urls.append(case.split('href=\'')[1].split('\'')[0])
        except:
            return urls

    return urls

def scan(scanner, domain):
    subdomains = set()

    for i in range(30): # TODO: use verbosity from `scanner` object
        results = set(askSearch('site%3A?+-www.?'.replace('?', domain), page = i))

        if len(results) == 0:
            break

        subdomains.update(results)

    return subdomains

