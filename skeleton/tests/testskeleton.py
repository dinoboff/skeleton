import os
import string
import unittest

from skeleton import Skeleton, Var
from skeleton.tests.utils import TestCase



class Static(Skeleton):
    src = 'skeletons/static'
    
    def template_formatter(self, template):
        return string.Template(template).substitute(self)


class MissingSkeleton(Static):
    src = 'skeletons/missing'


class DynamicContent(Static):
    src = 'skeletons/dynamic-content'
    vars = [
        Var('baz', 'Dummy variable')
        ]


class DynamicFileName(Static):
    src = 'skeletons/dynamic-file-name'


class TestSkeleton(TestCase):
        
    def test_write_with_missing_skeleton(self):
        s = MissingSkeleton()
        self.assertRaises(AttributeError, s.write, self.tmp_dir.path)
        
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

    def test_write_dynamic_content_with_var(self):
        resps = ['<input replacement>']
        self.input_mock.side_effect = lambda x: resps.pop(0)
        
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