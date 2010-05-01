import unittest

from skeleton import Skeleton


class TestDefaultTemplate(unittest.TestCase):

    def test_template_formatter(self):
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        s = Skeleton(bar="substituted")
        self.assertEqual(
            s.template_formatter("""foo {bar} baz"""), """foo substituted baz""")

    def test_template_formatter_raise_key_error(self):
        # skip test on python 2.5
        if not hasattr('', 'format'):
            return
        s = Skeleton(bar="substituted")
        self.assertRaises(KeyError,
            s.template_formatter, """foo {bar} {fooz} baz""")


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestDefaultTemplate)

if __name__ == "__main__":
    unittest.main()