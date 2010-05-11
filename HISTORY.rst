History
=======

0.5.1 (Mai 11, 2010)
--------------------

- Fix syntax error in the package virtualenvwrapper.project extension.


0.5 (Mai 10, 2010)
------------------

- Drop Python 2.5 support (might get basic support back).
- Various internal changes prior to 1.0 release.
- Improve error related to unexpected variable names in templates
  and file names


0.4 (Mai 8, 2010)
-----------------

- Convert Var names to lower_case_with_underscores.
- improve Var name display in command
- improve long string option for Vars in command line.
- fix bug in setup.py_tmpl of the mkmodule.py example.


0.3 (Mai 6, 2010)
-----------------

- New class method, `Skeleton.cmd` to create the logger and optparser.
- `Skeleton.run` doesn't set the logger and optparser anymore.
- `Skeleton.write` raises a KeyError exception if a key is missing
  instead of prompting the user.
- Removed the `pre_run`, `post_write` and `pre_write` methods. Overwrite
  the `write` and `run` instead.
- Added configure_parser() to configure the parser set by `Skeleton.cmd`.
- Add required_skeleton attribute to Skeleton. These skeleton will be run
  before the main. They all share the same entries.
- Added verbose options to the Skeleton optparser.
- Added a basic package template extension for `virtualenwrapper.project`.


0.2.1 (Mai 2, 2010):
--------------------

- Fix bug with Var._prompt static method which was preventing the prompt for 
  variable assignement.


0.2 (Mai 1, 2010):
-------------------

- Add python 3 support.


0.1 (April 31, 2010):
----------------------

- first release.
