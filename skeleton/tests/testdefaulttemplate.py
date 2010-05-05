"""
Test The default template formatter.
"""
import sys
import unittest

from skeleton import Skeleton, Var


class WithDefault(Skeleton):
    """
    A Skeleton with default variables
    """
    vars = [Var('bar', default='bar')]


class TestDefaultTemplate(unittest.TestCase):
    """
    Test for the default template formatter
    """

    def test_template_formatter(self):
        """
        Test template formatting
        """
        # skip test on python 2.5
        if sys.version_info < (2, 6):
            return
        skel = Skeleton(bar="substituted")
        self.assertEqual(
            skel.template_formatter("""foo {bar} baz"""),
            """foo substituted baz""")

    def test_formatter_raise_key_error(self):
        """
        Test template formatting a variable not set
        """
        # skip test on python 2.5
        if sys.version_info < (2, 6):
            return
        skel = Skeleton(bar="substituted")
        self.assertRaises(KeyError,
            skel.template_formatter, """foo {bar} {fooz} baz""")

    def test_template_use_default(self):
        """
        Test the template uses the default value if the variable is not set
        """
        # skip test on python 2.5
        if sys.version_info < (2, 6):
            return
        skel = WithDefault()
        self.assertEqual(
            skel.template_formatter("""foo {bar} baz"""),
            """foo bar baz""")


def suite():
    """
    Return all default formatter tests
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestDefaultTemplate)

if __name__ == "__main__":
    unittest.main()
