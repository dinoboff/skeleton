'''
Created on Apr 29, 2010

@author: dinoboff
'''
from __future__ import with_statement

import shutil
import tempfile
import unittest


from skeleton import Skeleton
import os


class TempDir(object):
    
    def create(self):
        self.path = tempfile.mkdtemp()
        return self.path
    
    def remove(self):
        shutil.rmtree(self.path)
        
    __enter__ = create
        
    def __exit__(self, type, value, traceback):
        self.remove()


class Static(Skeleton):
    src = 'skeletons/static'


class DynamicContent(Skeleton):
    src = 'skeletons/dynamic-content'


class TestSkeleton(unittest.TestCase):
    
    def setUp(self):
        super(TestSkeleton, self).setUp()
        self.tmp_dir = TempDir()
        self.tmp_dir.create()
        
    def tearDown(self):
        super(TestSkeleton, self).tearDown()
        self.tmp_dir.remove()

    def test_write_static_file(self):
        s= Static()
        s.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'baz'
            )

    def test_write_dynamic_content(self):
        s= DynamicContent(baz="<replaced>")
        s.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'foo <replaced> bar'
            )

    def test_write_dynamic_file_names(self):
        s= Static()
        s.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'baz'
            )

if __name__ == "__main__":
    unittest.main()