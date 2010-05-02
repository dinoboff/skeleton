"""
Created on May 2, 2010

@author: dinoboff
"""
from os import path
import unittest


from skeleton.tests.utils import TestCase
from skeleton.examples.license import BSD, BSD_THIRD_CLAUSE


class TestBSD(TestCase):
    """Test BSD Skeleton class"""

    def test_write_2clause(self):
        """Test write of a 2-clauses BSD license."""
        # skip test on Python 2.5
        if not hasattr('', 'format'):
            return
        variables = {
            'Author': 'Damien Lebrun',
            'Organization': '',
            }
        skel = BSD(variables)
        skel.write(self.tmp_dir.path)

        self.assertEqual(skel['ThirdClause'], '')
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))

    def test_write_3clause(self):
        """Test write of a 3-clauses BSD license."""
        # skip test on Python 2.5
        if not hasattr('', 'format'):
            return
        variables = {
            'Author': 'Damien Lebrun',
            'Organization': 'Foo inc',
            }
        skel = BSD(variables)
        skel.write(self.tmp_dir.path)

        self.assertEqual(
            skel['ThirdClause'],
            BSD_THIRD_CLAUSE.format(Organization='Foo inc')
            )
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
