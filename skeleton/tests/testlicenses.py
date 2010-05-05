"""
Tests the BDS, GPL and LGPL skeleton
"""

from os import path
import sys
import unittest


from skeleton.tests.utils import TestCase
from skeleton.examples.licenses import BSD, BSD_THIRD_CLAUSE, GPL, LGPL, \
    NoLicense, LicenseChoice


class TestBSD(TestCase):
    """Test skeleton.example.license.BSD."""

    def test_write_2clause(self):
        """Test write of a 2-clauses BSD license."""
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
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
        if sys.version_info < (2, 6):
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
        if sys.version_info < (2, 6):
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
        if sys.version_info < (2, 6):
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
        if sys.version_info < (2, 6):
            return

        variables = {
            'Author': 'Damien Lebrun',
            }

        skel = NoLicense(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))


class TestLicenseChoice(TestCase):
    """
    Test the LicenseChoice skeleton.
    """

    def test_licence_skel_default(self):
        """Test the default license_ske property"""
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'ProjectName': 'Foo',
            'Author': 'Damien Lebrun',
            }

        skel = LicenseChoice(variables)
        self.assertTrue(isinstance(skel.license_skel, NoLicense))
        self.assertEqual(skel.license_skel['Author'], 'Damien Lebrun')


    def test_bsd_licence_skel(self):
        """Test for a BSD license_ske property"""
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'ProjectName': 'Foo',
            'Author': 'Damien Lebrun',
            'License': 'BSD'
            }

        skel = LicenseChoice(variables)
        self.assertTrue(isinstance(skel.license_skel, BSD))

    def test_gpl_licence_skel(self):
        """Test for a GPL license_ske property"""
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'ProjectName': 'Foo',
            'Author': 'Damien Lebrun',
            'License': 'GPL'
            }

        skel = LicenseChoice(variables)
        self.assertTrue(isinstance(skel.license_skel, GPL))

    def test_lgpl_licence_skel(self):
        """Test for a LGPL license_ske property"""
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'ProjectName': 'Foo',
            'Author': 'Damien Lebrun',
            'License': 'LGPL'
            }

        skel = LicenseChoice(variables)
        self.assertTrue(isinstance(skel.license_skel, LGPL))

    def test_lgpl_run(self):
        """
        Test run of a LicenceChoice with license set to "LGPL"
        """
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        resps = ['Foo', 'Damien Lebrun', 'dinoboff@gmail.com', 'LGPL', ]
        self.input_mock.side_effect = lambda x: resps.pop(0)

        skel = LicenseChoice()
        skel.run(self.tmp_dir.path)

        self.assertEqual(self.input_mock.call_count, 4)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'COPYING')))
        self.assertTrue(
            path.exists(path.join(self.tmp_dir.path, 'COPYING.LESSER')))

    def test_lgpl_write(self):
        """
        Test write of a LicenceChoice with license set to "LGPL"
        """
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'ProjectName': 'Foo',
            'Author': 'Damien Lebrun',
            'License': 'LGPL'
            }

        skel = LicenseChoice(variables)
        skel.write(self.tmp_dir.path)

        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'LICENSE')))
        self.assertTrue(path.exists(path.join(self.tmp_dir.path, 'COPYING')))
        self.assertTrue(
            path.exists(path.join(self.tmp_dir.path, 'COPYING.LESSER')))

    def test_lgpl_write_fails(self):
        """
        Test write of a LicenceChoice fails if a key is missing
        """
        # skip test on Python 2.5
        if sys.version_info < (2, 6):
            return

        variables = {
            'Author': 'Damien Lebrun',
            'License': 'LGPL'
            }

        skel = LicenseChoice(variables)
        self.assertRaises(KeyError, skel.write, self.tmp_dir.path)


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
