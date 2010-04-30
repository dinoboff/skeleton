from __future__ import with_statement

import os

from skeleton import Skeleton, Var


NS_HEADER = """
__import__('pkg_resources').declare_namespace(__name__)
"""

class BasicPackage(Skeleton):
    src = 'basic-package'
    vars = [
        Var('ProjectName'),
        Var('PackageName'),
        Var('Author'),
        Var('AuthorEmail')
        ]
        
    def pre_write(self, dst_dir):
        self['NSPackages'] = []
        self['Packages'] = []
        
        # Create namespace packages
        current_ns = []
        package_path = self['PackageName'].split('.')
        for p in package_path[:-1]:
            current_ns.append(p)
            ns = '.'.join(current_ns)
            self['NSPackages'].append(ns)
            self['Packages'].append(ns)
            self._create_package(os.path.join(dst_dir, *current_ns), NS_HEADER)
        
        # Create package 
        self._create_package(os.path.join(dst_dir, *package_path))
    
    def _create_package(self, path, init_body=''):
        os.mkdir(path)
        with open(os.path.join(path, '__init__.py'), 'w') as f:
            f.write(init_body)


def main():
    BasicPackage().run()

if __name__ == '__main__':
    main()