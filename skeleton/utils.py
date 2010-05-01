import logging
import optparse
import os
import re
import stat
import sys


VALID_OPTION_NAME = re.compile("[a-z]([\w\d]*[a-z0-9])?",re.IGNORECASE)

def get_loggger(name):
    logger = logging.getLogger(name)
    logger.addHandler(NullHandler())
    return logger

def vars_to_optparser(vars):
    parser = optparse.OptionParser()
    for var in vars:
        if not VALID_OPTION_NAME.match(var.name):
            continue
        parser.add_option(
            "--%s" % var.name.replace('_', '-'),
            dest=var.name,
            help=var.full_description)
    return parser

def get_file_mode(path):
    stat.S_IMODE(os.stat(path)[stat.ST_MODE])


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def prompt(prompt_):
    result = raw_input(prompt_)
    try:
        return result.decode(sys.stdin.encoding)
    except AttributeError:
        return result