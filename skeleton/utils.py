"""
Skeleton Helpers
"""

from __future__ import with_statement
from contextlib import closing
import codecs
import logging
import optparse
import os
import re
import stat
import sys


VALID_OPTION_NAME = re.compile("[a-z]([\w\d]*[a-z0-9])?", re.IGNORECASE)

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

def insert_into_file(
    file_path, marker, text,
    marker_tag="-*-", keep_indent=True, keep_marker=True, encoding="UTF-8"):
    """
    Insert text into file at specific markers.
    
    eg, for a file "test.txt" with::
    
        foo
        -*- Insert Here -*-
        baz
    
    `insert_into_file('test.txt', 'Insert Here', 'bar\n', keep_marker=False)`
    would result in::
    
        foo
        bar
        baz
    
    @param file_path: file to insert content into
    @type file_path: str
    
    @param marker: Marker too look for in the file
    @type marker: str
    
    @param text: text to insert in the file
    @type text: unicode
    
    @param marker_tag: text surrounding the marker
    @type marker_tag: str
    
    @param keep_indent: Should it insert the text with the same marker indent.
    @type keep_indent: bool
    
    @param keep_marker: Should the marker be removed
    @type keep_marker: bool
    
    @param encoding: file encoding.
    @type encoding: str
    """
    marker_pattern = re.escape('%s %s %s' % (marker_tag, marker, marker_tag,))
    marker_re = re.compile(r"^(\s*).*%s.*$" % marker_pattern)
    edited = False
    new_content = []
    with closing(codecs.open(file_path, 'r', encoding=encoding)) as opened_file:
        for line in opened_file:
            match = marker_re.match(line)
            if match is None:
                new_content.append(line)
                continue

            edited = True

            if keep_marker:
                new_content.append(line)

            if keep_indent:
                indent = match.groups()[0]
                new_content.append('%s%s' % (indent, text,))
            else:
                new_content.append(text)

    if not edited:
        return

    with closing(codecs.open(file_path, 'w', encoding=encoding)) as opened_file:
        for line in new_content:
            opened_file.write(line)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def prompt(prompt_):
    result = raw_input(prompt_)
    try:
        return result.decode(sys.stdin.encoding)
    except AttributeError:
        return result
