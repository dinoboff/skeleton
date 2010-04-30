import unittest

from skeleton import Template


class TestDefaultTemplate(unittest.TestCase):


    def test_substitute(self):
        t = Template("""foo {bar} baz""")
        self.assertEqual(
            t.substitute(bar="substituted", fooz="None"), """foo substituted baz""")

    def test_substitute_raise_key_error(self):
            t = Template("""foo {bar} {fooz} baz""")
            self.assertRaises(KeyError,
                t.substitute, bar="substituted")


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestDefaultTemplate)

if __name__ == "__main__":
    unittest.main()