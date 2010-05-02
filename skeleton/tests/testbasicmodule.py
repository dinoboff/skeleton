import os
import unittest

from skeleton.examples.mkmodule import BasicModule
from skeleton.tests.utils import TestCase


class TestBasicModule(TestCase):

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