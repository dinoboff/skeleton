"""
Test skeleton.examples.basicpackage
"""

import os
import unittest

from skeleton.examples.basicpackage import BasicPackage, main
from skeleton.tests.utils import TestCase


class TestBasicPackage(TestCase):
    """
    Test the BasicPackage Skeleton
    """

    def test_write(self):
        """
        Test skeleton.examples.basicpackage.BasicPackage with a single package
        """
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        variables = {
            'ProjectName': 'foo',
            'PackageName': 'foo',
            'Author': 'Damien Lebrun',
            'AuthorEmail': 'dinoboff@gmail.com',
            }
        skel = BasicPackage(variables)
        skel.write(self.tmp_dir.path)

        self.assertEqual(skel['NSPackages'], [])
        self.assertEqual(skel['Packages'], ['foo'])
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'distribute_setup.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'MANIFEST.in')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'README.rst')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'setup.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo/__init__.py')))

    def test_write_namespaces(self):
        """
        Test skeleton.examples.basicpackage.BasicPackage with namespaces
        """
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        variables = {
            'ProjectName': 'foo-bar-baz',
            'PackageName': 'foo.bar.baz',
            'Author': 'Damien Lebrun',
            'AuthorEmail': 'dinoboff@gmail.com',
            }
        skel = BasicPackage(variables)
        skel.write(self.tmp_dir.path)

        self.assertEqual(set(skel['NSPackages']), set(['foo', 'foo.bar']))
        self.assertEqual(
            set(skel['Packages']),
            set(['foo', 'foo.bar', 'foo.bar.baz']))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'distribute_setup.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'MANIFEST.in')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'README.rst')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'setup.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo/__init__.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo/bar/__init__.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo/bar/baz/__init__.py')))

    def test_main(self):
        """Test basicpackage.main() """
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return

        resps = ['foo', 'foo', 'Damien Lebrun', 'dinoboff@gmail.com']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        main([self.tmp_dir.path])

        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'distribute_setup.py')
            ))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'MANIFEST.in')
            ))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'README.rst')
            ))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'setup.py')
            ))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo/__init__.py')
            ))

def suite():
    """
    Return suite for skeleton.examples.basicpackage
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestBasicPackage)

if __name__ == "__main__":
    unittest.main()
