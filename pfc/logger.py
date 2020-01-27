import sys
from functools import partial

from pfc import colors

class Logger:
    def __init__(self):
        self.stdout = [sys.stdout]
        self.stderr = [sys.stderr]


    def debug(self, *data):
        return self._log_dynamic('debug', data)

    def info(self, *data):
        return self._log_dynamic('info', data)

    def warn(self, *data):
        return self._log_dynamic('warn', data)

    def error(self, *data):
        return self._log_dynamic('error', data)

    def fatal(self, *data):
        return self._log_dynamic('fatal', data)


    # for dynamically generated log functions
    def _log_dynamic(self, fname, data):
        settings = self._get_config()[fname]
        data = self._to_str(data)

        return self._log(settings.get('streams', self.stdout), data, settings.get('prefix', ' '), settings.get('color', ''), settings.get('reset', colors.reset))

    # logs with a prefix and color and whatnot
    # `data` must be str
    def _log(self, streams, data, prefix, color, reset):
        message =  reset + '[' + color + prefix + reset + ']' + reset + ' ' + color + data + colors.reset
        self._write(streams, message)

    def _get_config(self):
        return {
            'debug' : {
                'prefix' : '/'
            },

            'info' : {
                'prefix' : '*',
                'color' : colors.fg_green
            },

            'warn' : {
                'prefix' : '!',
                'color' : colors.fg_orange
            },

            'error' : {
                'prefix' : '-',
                'color' : colors.fg_red,
                'streams' : self.stderr
            },

            'fatal' : {
                'prefix' : '-',
                'color' : colors.bg_red,
                'reset' : colors.bg_red
            }
        }

    def _to_str(self, msg):
        output = []

        for data in msg:
            # convert bytes to str
            if isinstance(data, bytes):
                data = data.decode('utf-8', errors = 'ignore')
            # otherwise, convert to str with repr
            elif not isinstance(data, str):
                data = repr(data)

            output.append(str(data))

        return ' '.join(output)

    def _write(self, streams, data):
        # convert to list so that we can support multiple streams
        if not isinstance(streams, list):
            streams = [streams]

        # write to all inputted streams
        for stream in streams:
            stream.write(data + '\n')


_default_logger = Logger()

debug = _default_logger.debug
info = _default_logger.info
warn = _default_logger.warn
error = _default_logger.error
fatal = _default_logger.fatal
