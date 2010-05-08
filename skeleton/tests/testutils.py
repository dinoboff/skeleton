"""
Test in skeleton.utils.*
"""
from __future__ import with_statement
import optparse
import os
import unittest

from skeleton import Var
from skeleton.tests.utils import TestCase
from skeleton.utils import insert_into_file, vars_to_optparser


class TestInsertIntoFile(TestCase):
    """Tests for in skeleton.utils.insert_into_file"""

    def test_insert_into_file(self):
        """test skeleton.insert_into_file()"""
        target = os.path.join(self.tmp_dir.path, 'test.txt')
        with open(target, 'w') as f_target:
            f_target.write("""foo\n# -*- insert here -*- #\nbaz\n""")

        insert_into_file(target, 'insert here', 'bar\n')
        with open(target) as f_target:
            self.assertEqual(
                f_target.readlines(),
                ['foo\n', '# -*- insert here -*- #\n', 'bar\n', 'baz\n']
                )

    def test_insert_with_indent(self):
        """test skeleton.insert_into_file() with indent to keep"""
        target = os.path.join(self.tmp_dir.path, 'test.txt')
        with open(target, 'w') as f_target:
            f_target.write("""foo\n  # -*- insert here -*- #\nbaz\n""")

        insert_into_file(target, 'insert here', 'bar\nfooz\n')
        with open(target) as f_target:
            self.assertEqual(
                f_target.read().strip(),
                'foo\n  # -*- insert here -*- #\n  bar\n  fooz\nbaz'
                )

    def test_insert_with_indent_to_lose(self):
        """test skeleton.insert_into_file() with indent to lose"""
        target = os.path.join(self.tmp_dir.path, 'test.txt')
        with open(target, 'w') as f_target:
            f_target.write("""foo\n  # -*- insert here -*- #\nbaz\n""")

        insert_into_file(target, 'insert here', 'bar\n', keep_indent=False)
        with open(target) as f_target:
            self.assertEqual(
                f_target.readlines(),
                ['foo\n', '  # -*- insert here -*- #\n', 'bar\n', 'baz\n']
                )

    def test_insert_and_remove_marker(self):
        """test skeleton.insert_into_file() with keep_marker off"""
        target = os.path.join(self.tmp_dir.path, 'test.txt')
        with open(target, 'w') as f_target:
            f_target.write("""foo\n# -*- insert here -*- #\nbaz\n""")

        insert_into_file(target, 'insert here', 'bar\n', keep_marker=False)
        with open(target) as f_target:
            self.assertEqual(
                f_target.readlines(),
                ['foo\n', 'bar\n', 'baz\n']
                )


class TestVarsToOptparser(unittest.TestCase):
    """
    Tests skeleton.utils.vars_to_optparser
    """

    def test_create_parser(self):
        """
        Tests vars_to_optparser create the OptParser if none are given
        """

        self.assertTrue(
            isinstance(vars_to_optparser([]), optparse.OptionParser)
            )

    def test_augment_parser(self):
        """
        Tests vars_to_optparser augment the parser given as argument
        """
        parser = optparse.OptionParser()
        self.assertTrue(vars_to_optparser([], parser) is parser)

    def test_pep8_var_name(self):
        """
        Tests long string formatting of options added by vars_to_optparser.
        
        All lower case with hyphen instead of underscore
        """
        parser = vars_to_optparser([Var('Foo'), Var('foo_bar')])
        self.assertEqual(parser.get_option('--foo').dest, 'Foo')
        self.assertEqual(parser.get_option('--foo-bar').dest, 'foo_bar')

    def test_default_metavar(self):
        parser = vars_to_optparser([Var('Foo'), Var('bar_name')])
        self.assertEqual(parser.get_option('--foo').metavar, 'FOO')
        self.assertEqual(parser.get_option('--bar-name').metavar, 'NAME')


def suite():
    """Return tests for skeleton.utils.*  """
    tests = unittest.TestSuite()
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestInsertIntoFile))
    tests.addTest(unittest.TestLoader().loadTestsFromTestCase(TestVarsToOptparser))
    return tests


if __name__ == "__main__":
    unittest.main()
