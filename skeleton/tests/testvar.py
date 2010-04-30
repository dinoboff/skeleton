'''
Created on Apr 29, 2010

@author: dinoboff
'''
import unittest

from mock import patch

from skeleton import Var

class TestVar(unittest.TestCase):

    def test_repr(self):
        v = Var('foo', description='dummy var')
        self.assertEqual(repr(v), '<Var foo default=None>')
        
    def test_full_description(self):
        v = Var('foo', description='dummy var')
        self.assertEqual(v.full_description(), 'foo (dummy var)')
        
    def test_full_description_without_description(self):
        v = Var('foo')
        self.assertEqual(v.full_description(), 'foo')
    
    @patch('__builtin__.raw_input')
    def test_prompt(self, input_mock):
        resps = ['', 'bar']
        input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo')
        self.assertEqual(v.prompt(), 'bar')
        
        self.assertEqual(input_mock.call_count, 2)
        for args in input_mock.call_args_list:
            self.assertEqual(args, (('Enter foo: ',),{},))
    
    @patch('__builtin__.raw_input')
    def test_prompt_with_default(self, input_mock):
        resps = ['']
        input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo', default='baz')
        self.assertEqual(v.prompt(), 'baz')
        
        self.assertEqual(input_mock.call_count, 1)
        for args in input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['baz']: """,),{},))
    
    @patch('__builtin__.raw_input')
    def test_prompt_with_empy_default(self, input_mock):
        resps = ['']
        input_mock.side_effect = lambda x: resps.pop(0)
        
        v = Var('foo', default='')
        self.assertEqual(v.prompt(), '')
        
        self.assertEqual(input_mock.call_count, 1)
        for args in input_mock.call_args_list:
            self.assertEqual(args, (("""Enter foo ['']: """,),{},))
    

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestVar)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()