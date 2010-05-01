'''
Created on Apr 29, 2010

@author: dinoboff
'''
import unittest

from skeleton import Var
from skeleton.tests.utils import TestCase

class TestVar(TestCase):

    def test_repr(self):
        v = Var('foo', description='dummy var')
        self.assertEqual(repr(v), '<Var foo default=None>')
        
    def test_full_description(self):
        v = Var('foo', description='dummy var')
        self.assertEqual(v.full_description, 'foo (dummy var)')
        
    def test_full_description_without_description(self):
        v = Var('foo')
        self.assertEqual(v.full_description, 'foo')
    
    def test_prompt(self):
        resps = ['', 'bar']
        self.input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo')
        self.assertEqual(v.prompt(), 'bar')
        
        self.assertEqual(self.input_mock.call_count, 2)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (('Enter foo: ',),{},))
    
    def test_prompt_with_default(self):
        resps = ['']
        self.input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo', default='baz')
        self.assertEqual(v.prompt(), 'baz')
        
        self.assertEqual(self.input_mock.call_count, 1)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['baz']: """,),{},))
    
    def test_prompt_with_empy_default(self):
        resps = ['']
        self.input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo', default='')
        self.assertEqual(v.prompt(), '')
        
        self.assertEqual(self.input_mock.call_count, 1)
        for args in self.input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['']: """,),{},))
    

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestVar)

if __name__ == "__main__":
    unittest.main()