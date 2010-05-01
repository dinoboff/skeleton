import os
import unittest

from skeleton.examples.basicpackage import BasicPackage
from skeleton.tests.utils import TestCase


class TestBasicPackage(TestCase):

    def test_write(self):
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        vars = {
            'ProjectName': 'foo',
            'PackageName': 'foo',
            'Author': 'Damien Lebrun',
            'AuthorEmail': 'dinoboff@gmail.com',
            }
        s = BasicPackage(vars)
        s.write(self.tmp_dir.path)
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'distribute_setup.py')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'MANIFEST.in')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'README.rst')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'setup.py')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'foo/__init__.py')))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestBasicPackage)

if __name__ == "__main__":
    unittest.main()