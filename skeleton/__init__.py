"""
Basic Template system for project skeleton.

skeleton is similar to the template part of PasteScript but 
without any dependencies; it should also be compatible with Python 3.

However in this early phase of development, it only target python 2.5+,
and tests require Mock.
"""

import codecs
import logging
import os
import re
import shutil
import sys

from skeleton.utils import get_loggger, get_file_mode, vars_to_optparser


log = get_loggger(__name__)


class Skeleton(dict):    
    """
    Skeleton Class.
    
    It should have a src attribute set to the path to the skeleton folder
    (relative to the class module) and a list of variables the skeleton template
    files require. The variable should be an object with a name attribute and
    prompt method than prompt the user for the variable value and return that
    value. You can use skeleton.Var.
    
    By default a template file ends with "_tmpl" (see the template_suffix 
    attribute), is UTF-8 encoded (file_encoding attribute) and will be formatted
    by python 2.6+ string Formatter.
    
    You can set an alternative formatter by overwriting the template_formatter
    method. It takes for argument the template to parse and self for
    variable mapping.
    """    
    src = None 
    vars = []
    template_suffix = '_tmpl'
    file_encoding = 'UTF-8'
    run_dry = False
        
    def pre_write(self, dst_dir): 
        """
        Called after the vars have been checked
        and before the creation of the files and directories.
        """
    
    def post_write(self, dst_dir):
        """
        Called after the files and directory have been created.
        """
    
    def pre_run(self, parser):
        """
        Called before parsing arguments and running Skeleton
        """

    def template_formatter(self, template):
        """
        Default template formatter.
        
        Require Python 2.6+
        """
        if not hasattr(template, 'format'):
            msg = (
                "%s's template_formatter expect a python 2.6+ string "
                "like object (with a format method).")
            log.critical(msg, self.__class__.__name__)
            raise NotImplementedError(msg % self.__class__.__name__)
        return template.format(**self)
    
    @property
    def skel_dir(self):
        """
        return the path (absolute path or relative to the current working
        directory).
        """
        if self.src is None:
            raise AttributeError("The src attribute of the %s Skeleton is not set" %
                self.__class__.__name__
                )
        mod = sys.modules[self.__class__.__module__]
        mod_dir = os.path.dirname(mod.__file__)
        return os.path.join(mod_dir, self.src)
    
    def write(self, dst_dir):
        """
        Copy files and folders from the skeleton folder to the dst_dir.
        
        The file name will be formatted by the template formatter so that file
        names can dynamically generated. Make sure that any special charters for
        the formatters are escaped.
        
        If the file name ends by "_tmpl" its content will be formatted by the
        template formatter.
        """
        log.info(
            "Rendering %s skeleton at %r...",
            self.__class__.__name__,
            dst_dir)
        
        if not os.path.exists(dst_dir):
            self._mkdir(dst_dir)
        
        self._check_vars()
        
        skel_dir = self.skel_dir
        skel_dir_len = len(skel_dir)
        log.debug("Getting skeleton from %r" % skel_dir)
        
        self.pre_write(dst_dir)
        for dir_path, dir_names, file_names in os.walk(skel_dir):
            rel_dir_path = dir_path[skel_dir_len:].lstrip(r'\/')
            
            #copy files
            for file_name in file_names:
                src = os.path.join(dir_path, file_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.template_formatter(file_name))
                self.copy_file(src, dst)
            
            #copy directories
            for dir_name in dir_names:
                src = os.path.join(dir_path, dir_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.template_formatter(dir_name))
                self._mkdir(dst, like=src)
        self.post_write(dst_dir)
    
    def copy_file(self, src, dst):
        if src.endswith(self.template_suffix):
            self._format_file(src, dst[:-len(self.template_suffix)])
        else:
            self._copy_file(src, dst)
        
    def _copy_file(self, src, dst):
        log.info("Copy %r to %r", src, dst)
        if not self.run_dry:
            shutil.copyfile(src , dst)
        self._set_mode(dst, like=src)
        
    def _format_file(self, src, dst):
        log.info("Creating %r from %r template...", dst, src)
        if not self.run_dry:
            fd_src = None
            fd_dst = None
            try:
                fd_src = codecs.open(src, encoding=self.file_encoding)
                fd_dst = codecs.open(dst, 'w', encoding=self.file_encoding)
                fd_dst.write(self.template_formatter(fd_src.read()))
            finally:
                if fd_src is not None:
                    fd_src.close()
                if fd_dst is not None:
                    fd_dst.close()
        self._set_mode(dst, like=src)
            
        
    def _mkdir(self, path, like=None):
        log.info("Create directory %r", path)
        if not self.run_dry:
            os.mkdir(path)
        if like is not None:
            self._set_mode(path, like)

    def _set_mode(self, path, like):
        log.info("Set mode of %r to %r", path, get_file_mode(like))
        if not self.run_dry:
            shutil.copymode(like, path)
        
    def _check_vars(self):
        for var in self.vars:
            if var.name in self:
                log.debug("Varaiable %r already set" % var.name)
                continue
            self[var.name] = var.prompt()
            
    def run(self, args=None):
        logging.basicConfig(level=logging.INFO)
        
        parser = vars_to_optparser(self.vars)
        parser.usage = "%prog [options] dst_dir"
        self.pre_run(parser)
        
        options, args = parser.parse_args(args)
        if len(args) != 1:
            parser.error("incorrect number of arguments")
        
        for var in self.vars:
            value = getattr(options, var.name)
            if value is not None:
                self[var.name] = value
        for k,v in self.items():
            print k,v
        self.write(args[0])
        


class Var(object):
    """Define a template variable."""

    def __init__(self, name, description=None, default=None):
        self.name = name
        self.description = description
        self.default = default

    def __repr__(self):
        return u'<%s %s default=%r>' % (
            self.__class__.__name__, self.name, self.default,)

    def full_description(self):
        if self.description:
            return u'%s (%s)' % (self.name, self.description,)
        else:
            return self.name
        
    def prompt(self):
        """Prompt the user for a value.
        
        If no default is defined, the user will be prompted until he gives a 
        value.
        """
        prompt = u'Enter %s' % self.full_description()
        if self.default is not None:
            prompt += u' [%r]' % self.default
        prompt += u': '
        
        while True:
            encoding = sys.stdout.encoding
            resp = raw_input(prompt.encode(encoding)).decode(encoding).strip()
            if resp:
                return resp
            elif self.default is not None:
                return self.default
            else:
                continue # persist asking
