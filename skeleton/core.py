"""
Core skeleton component
"""
import codecs
import collections
import datetime
import functools
import logging
import optparse
import os
import shutil
import sys
import weakref

from skeleton.utils import (
    get_loggger, get_file_mode, vars_to_optparser, prompt)


_LOG = get_loggger(__name__)


class SkeletonError(Exception):
    """Root exception"""


class TemplateKeyError(KeyError, SkeletonError):
    """Raised by Skeleton when a template required an unknown variable
    """

    #: Name of the unexpected variable
    variable_name = None

    #: Path to the file which cannot be formatted
    file_path = None

    def __init__(self, variable_name, file_path):
        super(TemplateKeyError, self).__init__(variable_name)
        self.variable_name = variable_name
        self.file_path = file_path

    def __str__(self):
        return ("Found unexpected variable %r in %r."
            % (self.variable_name, self.file_path,))


class FileNameKeyError(KeyError, SkeletonError):
    """Raised by Skeleton when a file name cannot be formatted
    """

    #: Name of the unexpected variable
    variable_name = None

    #: Path to the file which the name cannot be formatted
    file_path = None

    def __init__(self, variable_name, file_path):
        super(FileNameKeyError, self).__init__(variable_name)
        self.variable_name = variable_name
        self.file_path = file_path

    def __str__(self):
        return ("Found unexpected variable %r in file name %r"
            % (self.variable_name, self.file_path))


class ValidateError(SkeletonError):
    """Raised if a variable value is invalid .
    """


def run_requirements_last(skel_method):
    """Decorator for Skeleton methods

    The return wrapper will run the same method of the required
    skeleton instances after the wrapped method exists.
    """
    def wrapper(self, *args, **kw):
        """Method wrapper."""
        result = skel_method(self, *args, **kw)
        for skel in self.required_skeletons_instances:
            if hasattr(skel, skel_method.__name__):
                getattr(skel, skel_method.__name__)(*args, **kw)
        return result
    functools.update_wrapper(wrapper, skel_method)
    return wrapper


def run_requirements_first(skel_method):
    """Decorator for Skeleton methods

    The return wrapper will first run the same method of the required
    skeleton instances.
    """
    def wrapper(self, *args, **kw):
        """Method wrapper."""
        for skel in self.required_skeletons_instances:
            if hasattr(skel, skel_method.__name__):
                getattr(skel, skel_method.__name__)(*args, **kw)
        return skel_method(self, *args, **kw)
    functools.update_wrapper(wrapper, skel_method)
    return wrapper


class Skeleton(collections.MutableMapping):
    """Skeleton Class.

    It should have a `src` attribute set to the path to the skeleton folder
    (relative to the class module) and a list of variables, the `variables`
    attribute, the skeleton template files require. The variable should be an
    object with `name`, `display_name` and `full_description` attributes,
    and a prompt method which prompt the user for the variable value
    and return it. You can use `skeleton.Var`.

    By default a template file ends with "_tmpl" (see the `template_suffix`
    attribute), is UTF-8 encoded (`file_encoding` attribute) and will be
    formatted by Python 2.6+ string Formatter.

    You can set an alternative formatter by overwriting the
    `template_formatter` method. It takes for argument the template to parse
    and self for variable mapping.

    If the skeleton require other skeleton to be run first, list them in the
    required_skeletons attribute.
    """

    #: Path to skeleton folder, relative to Skeleton module
    src = None

    #: List of variable required by templates
    variables = []

    #: List of Skeleton to apply first
    required_skeletons = []

    #: Encoding of template file (UTF-8 by default)
    file_encoding = 'UTF-8'

    template_suffix = '_tmpl'
    run_dry = False

    def __init__(self, skeleton=None, **kw):
        self._required_skeletons_instances = None
        self._defaults = {}

        if isinstance(skeleton, Skeleton):
            self.set_variables = weakref.proxy(skeleton)
        else:
            self.set_variables = {'year': datetime.datetime.utcnow().year}
            if skeleton is not None:
                self.set_variables.update(skeleton)
        self.set_variables.update(kw)

        for var in self.variables:
            if var.default is not None:
                self._defaults[var.name] = var.default

    @property
    def required_skeletons_instances(self):
        """
        Return the skeletons required by this skeleton
        """
        if self._required_skeletons_instances is None:
            self._required_skeletons_instances = []
            for skel_class in self.required_skeletons:
                skel = skel_class(self)
                self._required_skeletons_instances.append(skel)
        return self._required_skeletons_instances

    @property
    def real_src(self):
        """
        Absolute Path to skeleton directory (read-only).
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

    def __contains__(self, key):
        return key in self.set_variables or key in self._defaults

    def __delitem__(self, key):
        self.set_variables.__delitem__(key)

    def __getitem__(self, key):
        try:
            return self.set_variables[key]
        except KeyError:
            pass
        try:
            return self._defaults[key]
        except KeyError:
            pass
        raise KeyError("%s is not set and has no default value" % key)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.set_variables) + len(self._defaults)

    def __setitem__(self, key, value):
        self.set_variables[key] = value

    def keys(self):
        """
        Return names of variables that are set or have a value
        """
        return list(set(self.set_variables.keys() + self._defaults.keys()))

    def update(self, *args, **kw):
        """
        Update the set_variables attribute
        """
        self.set_variables.update(*args, **kw)

    @run_requirements_last
    def check_variables(self):
        """
        Raise a KeyError if any required variable is missing.
        """
        for var in self.variables:
            self.__getitem__(var.name)

    @run_requirements_last
    def get_missing_variables(self):
        """
        Prompt user for any missing variable
        (even the ones with a default value).
        """
        for var in self.variables:
            if var.name not in self.set_variables:
                self[var.name] = var.do_prompt()
            else:
                _LOG.debug("Variable %r already set", var.name)

    @run_requirements_first
    def write(self, dst_dir, run_dry=False):
        """Apply skeleton to `dst_dir`.

        Copy files and folders from the `src` folder to the `dst_dir`.
        If `dst_dir` doesn't exist, it will be created.

        The file name are formatted by the template formatter so that file
        names can do dynamically generated. Make sure that any special
        characters for the formatters are escaped.

        If the file name ends by "_tmpl" its content will be formatted by the
        template formatter.

        Raises:

        - `KeyError` if a variable is missing and doesn't have a default.
        - `TemplateKeyError` if it found an unexpected variable in a template.
        - `FileNameKeyError` if it found an unexpected variable in a file name.
        - IOError if it cannot read the skeleton files, or cannot create
          files and folder.
        """
        self.run_dry = run_dry

        _LOG.info(
            "Rendering %s skeleton at %r...",
            self.__class__.__name__,
            dst_dir)

        self.check_variables()

        if not os.path.exists(dst_dir):
            self._mkdir(dst_dir)

        real_src = self.real_src
        real_src_len = len(real_src)
        _LOG.debug("Getting skeleton from %r" % real_src)

        for dir_path, dir_names, file_names in os.walk(real_src):
            rel_dir_path = dir_path[real_src_len:].lstrip(r'\/')

            #copy files
            for file_name in file_names:
                src = os.path.join(dir_path, file_name)
                dst = os.path.join(
                    dst_dir,
                    rel_dir_path,
                    self._format_file_name(file_name, dir_path)
                    )
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
        """Like write() but prompt user for missing variables.

        Raises:

        - `TemplateKeyError` if it found an unexpected variable in a template.
        - `FileNameKeyError` if it found an unexpected variable in a file name.
        - IOError if it cannot read the skeleton files, or cannot create
          files and folder.
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

        for var in skel.variables:
            value = getattr(options, var.name)
            if value is not None:
                skel[var.name] = value

        skel.run(args[0])

    def configure_parser(self):
        """Configure parser for Skeleton.cmd().
        """
        parser = optparse.OptionParser(usage="%prog [options] dst_dir")
        parser.add_option("-q", "--quiet",
            action="store_const", const=logging.FATAL, dest="verbose_")
        parser.add_option("-v", "--verbose",
            action="store_const", const=logging.INFO, dest="verbose_")
        parser.add_option("-d", "--debug",
            action="store_const", const=logging.DEBUG, dest="verbose_")
        parser.set_default('verbose_', logging.ERROR)

        parser = vars_to_optparser(self.variables, parser=parser)
        return parser

    def template_formatter(self, template):
        """Return a formatted version of of the string `template`.

        Raises a KeyError if a variable is missing.
        """
        return template.format(**self)

    def _format_file_name(self, file_name, dir_path):
        try:
            return self.template_formatter(file_name)
        except (KeyError,), exc:
            raise FileNameKeyError(
                exc.args[0],
                os.path.join(dir_path, file_name)
                )

    def _mkdir(self, path, like=None):
        """Create a directory (using os.mkdir)

        Only log the event if self.run_dry is True.
        """
        _LOG.info("Create directory %r", path)
        if not self.run_dry and not os.path.exists(path):
            os.mkdir(path)
        if like is not None:
            self._set_mode(path, like)

    def _copy_file(self, src, dst):
        """Copy src file to dst and format dst if src is a template.

        The template suffix should be removed from dst.
        """
        if dst.endswith(self.template_suffix):
            try:
                self._format_file(src, dst[:-len(self.template_suffix)])
            except (KeyError,), exc:
                raise TemplateKeyError(exc.args[0], src)
        else:
            self._copy_static_file(src, dst)

    def _copy_static_file(self, src, dst):
        """Copy file and mode.

        Only log the event if self.run_dry is True.
        """
        _LOG.info("Copy %r to %r", src, dst)
        if not self.run_dry:
            shutil.copyfile(src, dst)
        self._set_mode(dst, like=src)

    def _format_file(self, src, dst):
        """Copy src to dst and format it.

        Raises a KeyError if a variable is missing.
        """
        _LOG.info("Creating %r from %r template...", dst, src)
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
        _LOG.info("Set mode of %r to '%o'", path, get_file_mode(like))
        if not self.run_dry:
            shutil.copymode(like, path)


class Var(object):
    """Define a template variable.

    The variable names should follow pep8 guidelines about variable names.
    pep8 variable are easier to set with a Skeleton constructor and you should
    not assume the skeleton template formatter can use any name formatting.
    """
    _prompt = staticmethod(prompt)

    def __init__(self, name, description=None, default=None, intro=None):
        self.name = name
        self.description = description
        self.default = default
        self.intro = intro

    def __repr__(self):
        return u'<%s %s default=%r>' % (
            self.__class__.__name__, self.name, self.default,)

    @property
    def display_name(self):
        """Return a titled version of name were "_" are replace by spaces.

        Allows to get nice looking name at prompt while following pip8 guidance
        (a Var name can be use as argument of skeleton to set the variable).
        """
        return self.name.replace('_', ' ').title()

    @property
    def full_description(self):
        """Return the name of the variable and a description if description
        is set.
        """
        if self.description:
            return u'%s (%s)' % (self.display_name, self.description,)
        else:
            return self.display_name

    @property
    def prompt(self):
        """Message to Prompt"""
        prompt_ = u'Enter %s' % self.full_description
        if self.default is not None:
            prompt_ += u' [%r]' % self.default
        prompt_ += u': '
        return prompt_

    def do_prompt(self):
        """Prompt user for variable value and return the validated value

        It will keep prompting the user until it receive a valid value.
        By default, a value is valid if it is not a empty string string or if 
        the variable has a default.

        If the user value is empty and the variable has a default, the default
        value is returned.

        """
        if self.intro is not None:
            print self.intro

        prompt_ = self.prompt
        while True:
            try:
                return self.validate(self._prompt(prompt_))
            except (ValidateError,), exc:
                print str(exc)


    def validate(self, response):
        """Checks the user has given a non empty value or that the variable has
        a default.

        Returns the valide value or the default.

        Raises a ValidateError if the response is invalid.
        """
        if response:
            return response
        elif self.default is not None:
            return self.default
        else:
            raise ValidateError("%s is required" % self.display_name)


class Bool(Var):
    """Var accepting "y/n"

    """

    @property
    def full_description(self):
        """Return the name of the variable, a description if description
        is set, and the y/N choice.

        """
        if self.description:
            return u'%s (%s - y/N)' % (self.display_name, self.description,)
        else:
            return u'%s (y/N)' % self.display_name

    @property
    def prompt(self):
        """Message to Prompt (with default converted to "y" or "n")

        """
        prompt_ = u'Enter %s' % self.full_description
        if self.default is not None:
            prompt_ += u' [%r]' % (self.default and 'y' or 'N')
        prompt_ += u': '
        return prompt_

    def validate(self, response):
        """Checks the response is either Y, YES, N or NO, or that the variable
        has a default value.

        Raises a ValidateError exception if the response wasn't recognized or 
        if no value was given and one is required.

        """
        response = response.strip().upper()
        if response in ('Y', 'YES',):
            return True
        elif response in ('N', 'NO',):
            return False
        elif response == '':
            if self.default is not None:
                return self.default
            else:
                raise ValidateError("%s is required" % self.display_name)
        else:
            raise ValidateError('enter either "Y" for yes or "N" or no')
