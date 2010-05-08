"""
Tests for skeleton.examples.basicmodule module.
"""
import os
import sys
import unittest

from skeleton.examples.mkmodule import BasicModule
from skeleton.tests.utils import TestCase


class TestBasicModule(TestCase):
    """
    Test BasicModule Skeleton
    """

    def test_write(self):
        """
        Test BasicModule.write()
        """
        # skip test on python 2.5
        if sys.version_info < (2, 6):
            return
        variables = {
            'module_name': 'foo',
            'author': 'Damien Lebrun',
            'author_email': 'dinoboff@gmail.com',
            }
        skel = BasicModule(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'README.rst')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'setup.py')))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_dir.path, 'foo.py')))


def suite():
    """Return all tests for skeleton.examples.basicmodule module"""
    return unittest.TestLoader().loadTestsFromTestCase(TestBasicModule)

if __name__ == "__main__":
    unittest.main()
