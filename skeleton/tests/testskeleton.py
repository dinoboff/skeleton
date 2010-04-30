import os
import shutil
import string
import tempfile
import unittest

from mock import patch

from skeleton import Skeleton, Var



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
    
    def template_formatter(self, template):
        return string.Template(template).substitute(self)


class DynamicContent(Static):
    src = 'skeletons/dynamic-content'
    vars = [
        Var('baz', 'Dummy variable')
        ]


class DynamicFileName(Static):
    src = 'skeletons/dynamic-file-name'


class TestSkeleton(unittest.TestCase):
    
    def setUp(self):
        super(TestSkeleton, self).setUp()
        self.tmp_dir = TempDir()
        self.tmp_dir.create()
        
    def tearDown(self):
        super(TestSkeleton, self).tearDown()
        self.tmp_dir.remove()
        
    def test_write_with_dst_dir_to_create(self):
        s= Static()
        dst = os.path.join(self.tmp_dir.path, 'missing-dir')
        s.write(dst)
        self.assertEqual(
            open(os.path.join(dst, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(dst, 'bar/baz.txt')).read().strip(),
            'baz'
            )

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
        s= DynamicFileName(baz="replaced-name")
        s.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/replaced-name.txt')).read().strip(),
            'baz'
            )

    @patch('__builtin__.raw_input')
    def test_write_dynamic_content_with_var(self, input_mock):
        resps = ['<input replacement>']
        input_mock.side_effect = lambda x: resps.pop(0)
        
        s= DynamicContent()
        s.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'foo <input replacement> bar'
            )


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSkeleton)

if __name__ == "__main__":
    unittest.main()