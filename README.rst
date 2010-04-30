`skeleton` is similar to the template part of PasteScript_ but 
without any dependencies; it should also be compatible with Python 3.

However in this early phase of development, it only targets python 2.5+,
and its tests require Mock_.

Requirements
============

- Python 2.5+ (python 2.6+ to use the default template formatter)

It currently only has been tested with Python 2.6.2 on Mac OSX.


Installation
============

The easiest way to get skeleton is if you have setuptools / distribute_ or pip_ installed::

	easy_install skeleton

or::

	pip install skeleton

The current development version can be found at 
http://github.com/dinoboff/skeleton/tarball/master.


Usage example
=============

Let's create a basic module template; one with a `setup.py`, a `README` and the 
module files.

First, create the skeleton script layout::

	mkmodule.py
	module-skel/README
	module-skel/setup.py_tmpl
	module-skel/{ModuleName}.py

`mkmodule.py`
-------------

`mkmodule.py` is the script that create new module::

	#!/usr/bin/env python
	
	from skeleton import Skeleton, Var
	
	
	class SimpleModule(Skeleton):
	    src = 'module-skel'
	    vars = [
	        Var('ModuleName'),
	        Var('Author', default=''),
	        Var('AuthorEmail', default=''),
	        ]
	
	
	def main():
	    SimpleModule().run()
	    
	if __name__ == '__main__':
	    main()

The `src` attribute sets the relative path to the skeleton directory where the 
script will find the files and directories to create.

The `vars` attribute list the variables the templates will require.
The variables with a default can be left blank by the user.

`Skeleton.run()` is a convenient method to set an optparser and 
the logging basic config, and to apply the skeleton::

	Usage: mkmodule.py [options] dst_dir

	Options:
	  -h, --help            show this help message and exit
	  --ModuleName=MODULENAME
	                        ModuleName
	  --Author=AUTHOR       Author
	  --AuthorEmail=AUTHOREMAIL
	                        AuthorEmail
	
 
If you needed to run a `Skeleton` yourself, you would use the 
constructor, the `update` or `__setitem__` methods to set the variables
(`Skeleton` is a `dict` subclass), and the `write(dstdir)` method to apply
the skeleton.


`module-skel/README`
--------------------

`README` a is static file that will simply be copied::

	TODO: write the description of this module.
	
`module-skel/setup.py_tmpl`
---------------------------

`setup.py_tmpl` is a template (it ends with the _tmpl suffix) that will be used
to create a `setup.py` file::

	#!/usr/bin/env python

	from distutils.core import setup


	PROJECT = {ModuleName!r}
	VERSION = '0.1'
	AUTHOR = {Author!r}
	AUTHOR_EMAIL = {AuthorEmail!r}
	DESC = "A short description..."

	setup(
	    name=PROJECT,
	    version=VERSION,
	    description=DESC,
	    long_description=open('README.rst').read(),
	    author=AUTHOR,
	    author_email=AUTHOR_EMAIL,
	    py_module={ModuleName!r}
	)

By default, `Skeleton` uses python 2.6+ `string formatting`_.

`module-skel/{ModuleName}.py`
-----------------------------

`{ModuleName}.py` is the module file for which the name will be set dynamically
at run time.

.. NOTE::
	All file names are formatted using `Skeleton.template_formatter` method.
	Make sure to escape any special characters (with the default formatter,
	use `{{` to render `{` and `}}` for `}`).


TODO:
=====

- remove the Mock dependency.
- Write documentation.
- Learn to use the 2to3 script.
- Allow skeletons to chain each other (a skeleton could require).


Development
===========

Report any issues and fork `squeleton` at
http://github.com/dinoboff/skeleton/ .



.. _PasteScript: http://pythonpaste.org/script/
.. _pip: http://pip.openplans.org/
.. _distribute: http://packages.python.org/distribute/
.. _Mock: http://www.voidspace.org.uk/python/mock/
.. _string formatting: http://docs.python.org/library/functions.html#format