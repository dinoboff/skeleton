import os
import unittest

from skeleton.examples.basicmodule import BasicModule
from skeleton.tests.testskeleton import TempDir


class TestBasicModule(unittest.TestCase):
    
    def setUp(self):
        super(TestBasicModule, self).setUp()
        self.tmp_dir = TempDir()
        self.tmp_dir.create()
        
    def tearDown(self):
        super(TestBasicModule, self).tearDown()
        self.tmp_dir.remove()

    def test_write(self):
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        vars = {
            'ModuleName': 'foo',
            'Author': 'Damien Lebrun',
            'AuthorEmail': 'dinoboff@gmail.com',
            }
        s = BasicModule(vars)
        s.write(self.tmp_dir.path)

        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'README.rst')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'setup.py')))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir.path, 'foo.py')))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestBasicModule)

if __name__ == "__main__":
    unittest.main()