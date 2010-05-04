"""
Tests the BDS, GPL and LGPL skeleton
"""

from os import path
import unittest


from skeleton.tests.utils import TestCase
from skeleton.examples.licenses import BSD, BSD_THIRD_CLAUSE, GPL, LGPL, \
    NoLicense


class TestBSD(TestCase):
    """Test skeleton.example.license.BSD."""

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


class TestGPL(TestCase):
    """Test skeleton.example.license.GPL."""

    def test_write(self):
        """Test write of a GPL skeleton"""
        # skip test on Python 2.5
        if not hasattr('', 'format'):
            return

        variables = {
            'Author': 'Damien Lebrun',
            'ProjectName': 'Foo',
            }

        skel = GPL(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'COPYING')))


class TestLGPL(TestCase):
    """Test skeleton.example.license.LGPL."""

    def test_write(self):
        """Test write of a LGPL skeleton"""
        # skip test on Python 2.5
        if not hasattr('', 'format'):
            return

        variables = {
            'Author': 'Damien Lebrun',
            'ProjectName': 'Foo',
            }

        skel = LGPL(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'COPYING')))
        self.assertTrue(
            path.exists(path.join(self.tmp_dir.path, 'COPYING.LESSER')))


class TestNoLicense(TestCase):
    """
    Test the NoLicense skeleton.
    """

    def test_write(self):
        """Test write of a NoLicense skeleton"""
        # skip test on Python 2.5
        if not hasattr('', 'format'):
            return

        variables = {
            'Author': 'Damien Lebrun',
            }

        skel = NoLicense(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))

def suite():
    """Get all licence releated test"""
    tests = unittest.TestSuite()
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBSD))
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGPL))
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLGPL))
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestNoLicense))
    return tests

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
