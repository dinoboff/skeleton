"""
Basic Template system for project skeleton.

skeleton is similar to the template part of PasteScript but 
without any dependencies; it should also be compatible with Python 3.

However in this early phase of development, it only target python 2.5+,
and tests require Mock.
"""

import codecs
import datetime
import logging
import os
import re
import shutil
import sys

from skeleton.utils import get_loggger, get_file_mode, vars_to_optparser, prompt
import functools
import optparse


log = get_loggger(__name__)

def _run_requirement(skel_method):
    """
    Decorator for Skeleton methods
    
    The return wrapper will first run the same  method of the required
    templates.
    """
    def wrapper(self, *args, **kw):
        """Method wrapper."""
        for skel in self._required_skeletons:
            if hasattr(skel, skel_method.__name__):
                getattr(skel, skel_method.__name__)(*args, **kw)
            self.update(skel)
        return skel_method(self, *args, **kw)
    functools.update_wrapper(wrapper, skel_method)
    return wrapper


class Skeleton(dict):
    """
    Skeleton Class.
    
    It should have a `src` attribute set to the path to the skeleton folder
    (relative to the class module) and a list of variables, the `vars` 
    attribute, the skeleton template files require. The variable should be an 
    object with name and full_description attribute, and a prompt method than 
    prompt the user for the variable value and return it. You can use 
    `skeleton.Var`.
    
    By default a template file ends with "_tmpl" (see the `template_suffix` 
    attribute), is UTF-8 encoded (`file_encoding` attribute) and will be 
    formatted by Python 2.6+ string Formatter.
    
    You can set an alternative formatter by overwriting the `template_formatter`
    method. It takes for argument the template to parse and self for
    variable mapping.
    
    If the skeleton require other skeleton to be run first, list them in the
    required_skeletons attribute.
    """
    src = None
    vars = []
    required_skeletons = []
    template_suffix = '_tmpl'
    file_encoding = 'UTF-8'
    run_dry = False

    def __init__(self, *arg, **kw):
        super(Skeleton, self).__init__(*arg, **kw)

        self._required_skeletons = []
        for skel_class in self.required_skeletons:
            skel = skel_class(*arg, **kw)
            self.update(skel)
            self._required_skeletons.append(skel)

        # Set global variables
        self['year'] = datetime.datetime.utcnow().year

        # Set defaults
        self._defaults = dict([
            (var.name, var.default,)
                for var in self.vars if var.default is not None
                ])

    def update(self, *args, **kw):
        """
        Add or update entries to the skeleton and its required skeleton
        instances.
        
        See dict.update()
        """
        for skel in self._required_skeletons:
            skel.update(*args, **kw)
        super(Skeleton, self).update(*args, **kw)

    def __setitem__(self, key, value):
        """
        Add or update an entry in the skeleton and its required skeleton
        instances. 
        """
        for skel in self._required_skeletons:
            skel.__setitem__(key, value)
        super(Skeleton, self).__setitem__(key, value)

    def get(self, variable_name, default=None):
        """
        Get the set variable value or its default or the given default
        """
        default = self._defaults.get(variable_name, default)
        return super(Skeleton, self).get(variable_name, default)

    @property
    def skel_dir(self):
        """
        return the path (absolute path or relative to the current working
        directory).
        """
        if self.src is None:
            raise AttributeError(
                "The src attribute of the %s Skeleton is not set" %
                self.__class__.__name__
                )

        mod = sys.modules[self.__class__.__module__]
        mod_dir = os.path.dirname(mod.__file__)
        skel_path = os.path.join(mod_dir, self.src)

        if not os.path.exists(skel_path):
            raise AttributeError("No skeleton at %r" % skel_path)
        return skel_path

    @_run_requirement
    def check_vars(self):
        """
        Raise a KeyError if any required variable is missing.
        """
        for var in self.vars:
            if var.name not in self and var.name not in self._defaults:
                raise KeyError("Variable %r not set." % var.name)

    @_run_requirement
    def get_missing_variables(self):
        """
        Prompt user for any missing variable 
        (even the ones with a default value).
        """
        for var in self.vars:
            if var.name not in self:
                self[var.name] = var.prompt()
            else:
                log.debug("Varaiable %r already set", var.name)

    @_run_requirement
    def write(self, dst_dir, run_dry=False):
        """
        Apply skeleton to dst_dir.
        
        Copy files and folders from the src folder to the dst_dir. If dst_dir 
        doesn't exist, it will be created.
        
        The file name are formatted by the template formatter so that file
        names can do dynamically generated. Make sure that any special charters
        for the formatters are escaped.
        
        If the file name ends by "_tmpl" its content will be formatted by the
        template formatter.
        
        Raises:
        - KeyError if a variable is missing and doesn't have a default.
        - IOError if it cannot read the skeleton files, or cannot create
          files and folder.
        """
        self.run_dry = run_dry

        log.info(
            "Rendering %s skeleton at %r...",
            self.__class__.__name__,
            dst_dir)

        self.check_vars()

        if not os.path.exists(dst_dir):
            self._mkdir(dst_dir)

        skel_dir = self.skel_dir
        skel_dir_len = len(skel_dir)
        log.debug("Getting skeleton from %r" % skel_dir)

        for dir_path, dir_names, file_names in os.walk(skel_dir):
            rel_dir_path = dir_path[skel_dir_len:].lstrip(r'\/')

            #copy files
            for file_name in file_names:
                src = os.path.join(dir_path, file_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.template_formatter(file_name))
                self._copy_file(src, dst)

            #copy directories
            for dir_name in dir_names:
                src = os.path.join(dir_path, dir_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self.template_formatter(dir_name))
                self._mkdir(dst, like=src)

    def run(self, dst_dir, run_dry=False):
        """
        Like write() but prompt user for missing variables.
        """
        self.get_missing_variables()
        self.write(dst_dir, run_dry=run_dry)

    @classmethod
    def cmd(cls, argv=None):
        """
        Convenient method to set a logger, an optpaser and run the skeleton
        """

        skel = cls()

        parser = skel.configure_parser()
        options, args = parser.parse_args(argv)
        if len(args) != 1:
            parser.error("incorrect number of arguments")

        logging.basicConfig(
            level=options.verbose_,
            format="%(levelname)s - %(message)s"
            )

        for var in skel.vars:
            value = getattr(options, var.name)
            if value is not None:
                skel[var.name] = value

        skel.run(args[0])

    def configure_parser(self):
        """Configure parser for Skeleton.cmd()"""
        parser = optparse.OptionParser(usage="%prog [options] dst_dir")
        parser.add_option("-q", "--quiet",
            action="store_const", const=logging.FATAL, dest="verbose_")
        parser.add_option("-v", "--verbose",
            action="store_const", const=logging.INFO, dest="verbose_")
        parser.add_option("-d", "--debug",
            action="store_const", const=logging.DEBUG, dest="verbose_")
        parser.set_default('verbose_', logging.ERROR)

        parser = vars_to_optparser(self.vars, parser=parser)
        return parser

    def template_formatter(self, template):
        """
        Default template formatter.
        
        Require Python 2.6+
        """
        if sys.version_info < (2, 6):
            msg = (
                "%s's template_formatter expect a python 2.6+ string "
                "like object (with a format method).")
            log.critical(msg, self.__class__.__name__)
            raise NotImplementedError(msg % self.__class__.__name__)
        context = dict(self._defaults)
        context.update(self)
        return template.format(**context)

    def _mkdir(self, path, like=None):
        """
        Create a directory (using os.mkdir)
        
        Only log the event if self.run_dry is True.
        """
        log.info("Create directory %r", path)
        if not self.run_dry and not os.path.exists(path):
            os.mkdir(path)
        if like is not None:
            self._set_mode(path, like)

    def _copy_file(self, src, dst):
        """
        Copy src file to dst and format dst if src is a template.
        
        The template suffix should be removed from dst.
        """
        if dst.endswith(self.template_suffix):
            self._format_file(src, dst[:-len(self.template_suffix)])
        else:
            self._copy_static_file(src, dst)

    def _copy_static_file(self, src, dst):
        """
        Copy file and mode.
        
        Only log the event if self.run_dry is True.
        """
        log.info("Copy %r to %r", src, dst)
        if not self.run_dry:
            shutil.copyfile(src , dst)
        self._set_mode(dst, like=src)

    def _format_file(self, src, dst):
        """
        Copy src to dst and format it.
        
        Raises a KeyError if a variable is missing.
        """
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

    def _set_mode(self, path, like):
        """
        Set mode of `path` with the mode of `like`.
        """
        log.info("Set mode of %r to '%o'", path, get_file_mode(like))
        if not self.run_dry:
            shutil.copymode(like, path)


class Var(object):
    """
    Define a template variable.
    
    The variable names should follow pep8 guidelines about variable names.
    pep8 variable are easier to set with a Skeleton constructor and you should
    not assume the skeleton template formatter can use any name formatting.
    """
    _prompt = staticmethod(prompt)

    def __init__(self, name, description=None, default=None):
        self.name = name
        self.description = description
        self.default = default

    def __repr__(self):
        return u'<%s %s default=%r>' % (
            self.__class__.__name__, self.name, self.default,)

    @property
    def display_name(self):
        """
        Return a titled version of name were "_" are replace by space.
        
        Allows to get sice looking name at prompt while following pip8 quide
        (a Var name can be use as argument of skeleton to set to variable).
        """
        return self.name.replace('_', ' ').title()

    @property
    def full_description(self):
        """
        Return the name of the variable and short description if description
        is set.
        """
        if self.description:
            return u'%s (%s)' % (self.display_name, self.description,)
        else:
            return self.display_name

    def prompt(self):
        """Prompt the user for a value.
        
        If no default is defined, the user will be prompted until he gives a 
        value.
        """
        prompt_ = u'Enter %s' % self.full_description
        if self.default is not None:
            prompt_ += u' [%r]' % self.default
        prompt_ += u': '

        while True:
            resp = self._prompt(prompt_)
            if resp:
                return resp
            elif self.default is not None:
                return self.default
            else:
                continue # persist asking
