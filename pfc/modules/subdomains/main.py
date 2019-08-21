#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *
from . import sources

import re

def sanitize_cases(cases, domain = ''):
    output = set()

    for case in cases:
        if '://' in case:
            case = case.split('://', 1)[1]
        
        if '/' in case:
            case = case.split('/', 1)[0]

        case = case.strip().strip('.')

        if case.endswith('.' + domain) and re.match('^[a-zA-Z0-9]+[a-zA-Z0-9-._]*[a-zA-Z0-9]+$', case):
            output.add(case)

    return output

class SubdomainsModule(Module):
    def execute(self, context):
        output = list()

        for domain in context.args['domain']:
            domain = domain.strip().strip('.')

            subdomains = set()
            prev_size = len(subdomains)
    
            logging.info('Scanning for subdomains of %s ...' % domain)

            for source in sources.sources:
                try:
                    logging.debug('Scraping source %s for subdomains of %s' % (source.NAME, domain))
                    subdomains.update(sanitize_cases(source.scan(self, domain), domain))

                    logging.debug('Found %d new results.' % (len(subdomains) - prev_size))

                    prev_size = len(subdomains)
                except Exception as e:
                    logger.warn('Scraping of source %s failed.' % source.NAME, exc_info = True)

            output.extend(list(subdomains))
        
        context.output = output
        context.status = SUCCESS

        return context
