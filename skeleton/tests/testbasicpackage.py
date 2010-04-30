import os
import unittest

from mock import patch

from skeleton.examples.basicpackage import BasicPackage
from skeleton.tests.testskeleton import TempDir


class TestBasicPackage(unittest.TestCase):
    
    def setUp(self):
        super(TestBasicPackage, self).setUp()
        self.tmp_dir = TempDir()
        self.tmp_dir.create()
        
    def tearDown(self):
        super(TestBasicPackage, self).tearDown()
        self.tmp_dir.remove()

    def test_write(self):
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