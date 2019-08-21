#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

import requests

def get(url, headers = {}):
    return requests.get(url, headers = {**{
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }, **headers})

# TODO: finish library
def post(url, body = {}, headers = {}):
    logger.fatal('post: not implemented.')
    return None
