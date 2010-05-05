"""
Tests for skeleton.Var
"""
import unittest

from skeleton import Var
from skeleton.tests.utils import TestCase

class TestVar(TestCase):
    """
    Tests for skeleton.Var
    """

    def test_repr(self):
        """
        Tests Var representation
        """
        var = Var('foo', description='dummy var')
        self.assertEqual(repr(var), '<Var foo default=None>')

    def test_full_description(self):
        """
        Tests Var full description (complete)
        """
        var = Var('foo', description='dummy var')
        self.assertEqual(var.full_description, 'foo (dummy var)')

    def test_basic_full_description(self):
        """
        Tests Var full description (missing description)
        """
        var = Var('foo')
        self.assertEqual(var.full_description, 'foo')

    def test_prompt(self):
        """
        Tests Var.prompt()
        """
        resps = ['', 'bar']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        var = Var('foo')
        self.assertEqual(var.prompt(), 'bar')

        self.assertEqual(self.input_mock.call_count, 2)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (('Enter foo: ',), {},))

    def test_prompt_with_default(self):
        """
        Test Var.prompt() without default
        """
        resps = ['']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        var = Var('foo', default='baz')
        self.assertEqual(var.prompt(), 'baz')

        self.assertEqual(self.input_mock.call_count, 1)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['baz']: """,), {},))

    def test_prompt_empty_default(self):
        """
        Test Var.prompt() with empty default
        """
        resps = ['']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        var = Var('foo', default='')
        self.assertEqual(var.prompt(), '')

        self.assertEqual(self.input_mock.call_count, 1)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['']: """,), {},))


def suite():
    """Return all Var tests"""
    return unittest.TestLoader().loadTestsFromTestCase(TestVar)

if __name__ == "__main__":
    unittest.main()
