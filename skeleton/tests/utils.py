import unittest
import __builtin__
import tempfile
import shutil


class RawInputMock(object):
    
    def __init__(self):
        self.return_value = None
        self.side_effect = None
        self.call_args_list = []
        
    def __call__(self, *args, **kw):
        self.call_args_list.append((args,kw,))
        
        if self.side_effect is not None:
            return self.side_effect(*args, **kw)
        elif self.return_value is not None:
            return self.return_value
        else:
            raise Exception("No return value or side effect set.")

    @property
    def call_count(self):
        return len(self.call_args_list)
    
    @property
    def called(self):
        return self.call_count > 0


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
        __builtin__.raw_input = self.input_mock = RawInputMock()
        
    def tearDown(self):
        super(TestCase, self).tearDown()
        self.tmp_dir.remove()
        __builtin__.raw_input = self._input
