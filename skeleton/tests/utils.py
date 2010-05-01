import unittest
import __builtin__
import tempfile
import shutil

from mock import Mock

class TempDir(object):
    
    def create(self):
        self.path = tempfile.mkdtemp()
        return self.path
    
    def remove(self):
        shutil.rmtree(self.path)
        
    __enter__ = create
        
    def __exit__(self, type, value, traceback):
        self.remove()


class TestCase(unittest.TestCase):
    
    def setUp(self):
        super(TestCase, self).setUp()
        self.tmp_dir = TempDir()
        self.tmp_dir.create()
        self._input = __builtin__.raw_input
        __builtin__.raw_input = self.input_mock = Mock()
        
    def tearDown(self):
        super(TestCase, self).tearDown()
        self.tmp_dir.remove()
        __builtin__.raw_input = self._input