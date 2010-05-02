from __future__ import with_statement

import os
import urllib

from skeleton import Skeleton, Var
from skeleton.utils import get_loggger
import logging


log = get_loggger(__name__)

NS_HEADER = """
__import__('pkg_resources').declare_namespace(__name__)
"""

DISTRIBUTE_SETUP_URL = 'http://nightly.ziade.org/distribute_setup.py'

class BasicPackage(Skeleton):
    """
    Create a new package package (with namespace support) with the setup.py,
    README.rst and MANIFEST.in files already setup.
    
    Require the following variables:
    
    - ProjectName;
    - PackageName;
    - Author;
    - and AuthorEmail.
    
    Todo: Allow to set defaults for AUthor and AuthorEmail.
    Todo: Better README.rst content like Having a basic Installation and
    requirement section.
    Todo: Setup a test package and the distribute use_2to3 option.
    """
    
    src = 'basic-package'
    vars = [
        Var('ProjectName'),
        Var('PackageName'),
        Var('Author'),
        Var('AuthorEmail')
        ]
        
    def pre_write(self, dst_dir):
        self._create_package_and_namespaces(dst_dir)
        self._get_distribute(dst_dir)
    
    def _create_package_and_namespaces(self, dst_dir):
        self['NSPackages'] = []
        self['Packages'] = []
        
        # Create namespace packages
        current_ns = []
        package_part = self['PackageName'].split('.')
        for p in package_part[:-1]:
            current_ns.append(p)
            self['NSPackages'].append('.'.join(current_ns))
            self._create_package(dst_dir, current_ns, NS_HEADER)
        
        # Create package 
        self._create_package(dst_dir, package_part)
    
    def _create_package(self, dst_dir, package_part, init_body=''):
        path = os.path.join(dst_dir, *package_part)
        package = '.'.join(package_part)
        self['Packages'].append(package)
        
        log.info("Creating package %s" % package)
        if self.run_dry:
            return
        os.mkdir(path)
        with open(os.path.join(path, '__init__.py'), 'w') as f:
            f.write(init_body)
    
    def _get_distribute(self, dst_dir):
        log.info(
            'Getting "distribute_setup.py" from %r...'% DISTRIBUTE_SETUP_URL)
        urllib.urlretrieve(
            DISTRIBUTE_SETUP_URL,
            os.path.join(dst_dir, 'distribute_setup.py'))


def virtualenv_warpper_hook(args):
    """
    Create a new package package (with namespace support)
    with the setup.py, README.rst and MANIFEST.in files already setup.
    """
    logging.basicConfig(level=logging.INFO)
    BasicPackage().write('src/')


def main():
    BasicPackage().run()

if __name__ == '__main__':
    main()