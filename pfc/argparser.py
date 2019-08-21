#!/usr/bin/env python3

class ArgumentParser:
    def __init__(self, rules):
        self.rules = rules

        self.type_map = {
            'int' : int,
            'integer' : int,

            'str' : str,
            'string' : str,

            'bytes' : bytes, # TODO: use smartbytes

            'bool' : bool,
            'boolean' : bool,

            'float' : float,

            'list' : list,
            'array' : list,

            'set' : set,

            'tuple' : tuple,

            'range' : range,

            'zip' : zip

        }

    def parse(self, arguments):
        # make a copy of the list in memory
        arguments = arguments.copy()

        output = {
            None : list() # this is for the positional arguments that are undefined
        }

        found_rule = None
        current_argument_specifier = None
        positional_argument_index = 1

        # parse all arguments
        while len(arguments) != 0:
            argument = arguments.pop(0)

            # temporary variables
            argument_specifier = None
            
            # check each rule for a match
            for rule in self.rules:
                # make lists of name and shortnames to accept as argument specifiers
                name_argument_options = ['--' + rule['name']] + ['--' + str(x) for x in rule.get('aliases', [])]
                shortname_argument_options = (['-' + rule['shortname']] if 'shortname' in rule else []) + ['-' + str(x) for x in rule.get('shortaliases', [])]

                # check if this is an argument specifier
                if argument in (name_argument_options + shortname_argument_options):
                    argument_specifier = rule
                    break

            if argument_specifier and argument_specifier.get('arguments', 0) == 0:
                found_rule = argument_specifier
                argument_specifier = None
                argument = True
        
            # if there's already an argument specifier set
            if argument_specifier and not current_argument_specifier:
                current_argument_specifier = argument_specifier
                continue

            # otherwise, we should treat this as a string, not an argument
            argument_specifier = None

            # if there's an argument specifier set
            if current_argument_specifier and not found_rule:
                found_rule = current_argument_specifier
                current_argument_specifier = None

            # find a positional argument
            elif not found_rule:
                for rule in self.rules:
                    if positional_argument_index == rule.get('position', -1):
                        found_rule = rule

                        # rules with multiple set will stop incrementing the index
                        if not rule.get('multiple', False):
                            positional_argument_index += 1
                        
                        break

                # if we still haven't found one, just add to None

            # post processing
            name = (None if not found_rule else found_rule['name'])

            if found_rule:
                # value map (e.g. 'stdin' => 0, 'stdout' => 1, etc)
                if found_rule.get('map', None) and isinstance(found_rule.get('map', None), dict):
                    argument = found_rule.get('map', dict()).get(argument, argument)

                # convert to type
                argument = self.type_map[found_rule.get('type', 'str')](argument)
                
                # TODO: support validation

            # save the argument whether it's a list or (type)
            if found_rule and found_rule.get('multiple', False):
                if not isinstance(output.get(name, None), list):
                    output[name] = list()

                output[name].append(argument)
            else:
                output[name] = argument

        # fill in defaults in `output`
        for rule in self.rules:
            if 'default' in rule and not rule['name'] in output:
                output[rule['name']] = rule['default']

        return output

