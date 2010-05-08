"""
Test Skeleton base class
"""
from __future__ import with_statement
import os
import string
import unittest

from skeleton import Skeleton, Var
from skeleton.tests.utils import TestCase



class Static(Skeleton):
    """
    Skeleton with only static files:
    
    - foo.txt
    - bar/baz.txt
    """
    src = 'skeletons/static'

    def template_formatter(self, template):
        """
        Set a python 2.5 compatible formatter
        """
        context = dict(self._defaults)
        context.update(self)
        return string.Template(template).substitute(context)


class MissingSkeleton(Static):
    """
    Skeleton with invalid src attribute
    """
    src = 'skeletons/missing'


class DynamicContent(Static):
    """
    Skeleton dynamic content (bar/bax.txt_tmpl)
    """
    src = 'skeletons/dynamic-content'
    vars = [
        Var('baz', 'Dummy variable'),
        ]


class DynamicContentWithOptional(DynamicContent):
    """
    Skeleton with an optional variable.
    """
    vars = [
        Var('opional_var', default='<default>')
        ]


class DynamicFileName(Static):
    """
    Skeleton with a dynamic file name (bar/${baz}.txt)
    """
    src = 'skeletons/dynamic-file-name'


class Required(Static):
    """
    Just a ${FileName}.txt file.
    """
    src = "skeletons/required"
    vars = [ Var('file_name') ]


class StaticWithRequirement(Static):
    """
    Add the requirment to the Static class
    """
    required_skeletons = [Required]



class TestSkeleton(TestCase):
    """
    Test for skeleton.Skeleton
    """

    def test_default_variables(self):
        """Test Skeleton set the default Year variable."""
        skel = Skeleton()
        self.assertTrue('year' in skel)

    def test_write_without_src(self):
        """
        test skeleton src pointing to a missing folder
        """
        skel = MissingSkeleton()
        self.assertRaises(AttributeError, skel.write, self.tmp_dir.path)

    def test_write_missing_variable(self):
        """Test write raise KeyError if a variable is not set."""
        skel = DynamicContent()
        self.assertRaises(KeyError, skel.write, self.tmp_dir.path)

    def test_default_var_available1(self):
        """
        Check Skeleton.get() return the set value or its default
        """
        skel = DynamicContentWithOptional()
        self.assertEqual(skel.get('opional_var'), '<default>')

    def test_check_var_with_default_var(self):
        """
        Checks Skeleton.get() return the set value or its default
        """
        skel = DynamicContentWithOptional()
        try:
            skel.check_vars()
        except KeyError:
            self.fail("check_vars() should not raise KayError "
                "if the missing variable has a default.")


    def test_default_var_is_overwritten(self):
        """
        Tests the value given to the constructor overwrite the default.
        """
        skel = DynamicContentWithOptional()
        self.assertEqual(skel.get('opional_var'), '<default>')

        skel = DynamicContentWithOptional(opional_var='template value')
        self.assertEqual(skel.get('opional_var'), 'template value')

    def test_write_create_dst_dir(self):
        """
        tests Skeleton.write() create the missing dst directory
        """
        skel = Static()
        dst = os.path.join(self.tmp_dir.path, 'missing-dir')
        skel.write(dst)
        self.assertEqual(
            open(os.path.join(dst, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(dst, 'bar/baz.txt')).read().strip(),
            'baz'
            )

    def test_write_static_file(self):
        """
        Tests Skeleton.write() with static file
        """
        skel = Static()
        skel.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'baz'
            )

    def test_write_dynamic_content(self):
        """
        Tests Skeleton.write() with dynamic content.
        """
        skel = DynamicContent(baz="<replaced>")
        skel.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'foo <replaced> bar'
            )

    def test_write_dynamic_file_names(self):
        """
        Tests Skeleton.write() with dynamic file name
        """
        skel = DynamicFileName(baz="replaced-name")
        skel.write(self.tmp_dir.path)
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(
                self.tmp_dir.path,
                'bar/replaced-name.txt')
                ).read().strip(),
            'baz'
            )

    def test_run_with_var(self):
        """
        Test Skeleton.run() with dynamic content and variable prompt.
        """
        resps = ['<input replacement>']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        skel = DynamicContent()
        skel.run(self.tmp_dir.path)

        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'foo.txt')).read().strip(),
            'foo'
            )
        self.assertEqual(
            open(os.path.join(self.tmp_dir.path, 'bar/baz.txt')).read().strip(),
            'foo <input replacement> bar'
            )

    def test_get_variables_with_default(self):
        """Test prompt of variable with default"""
        resps = ['<input replacement>']
        self.input_mock.side_effect = lambda x: resps.pop(0)

        skel = DynamicContentWithOptional()

        skel.get_missing_variables()
        self.assertEqual(self.input_mock.call_count, 1)
        self.assertEqual(skel.get('opional_var'), '<input replacement>')

    def test_write_required_skel(self):
        """
        Test it write the of required 
        """
        skel = StaticWithRequirement(file_name="fooz")
        skel.write(self.tmp_dir.path)
        self.assertTrue(
            os.path.exists(os.path.join(self.tmp_dir.path, 'foo.txt')))
        self.assertTrue(
            os.path.exists(os.path.join(self.tmp_dir.path, 'bar/baz.txt')))
        self.assertTrue(
            os.path.exists(os.path.join(self.tmp_dir.path, 'fooz.txt')))

    def test_overwrite_required_skel(self):
        """
        Test it write the of required 
        """
        skel = StaticWithRequirement(file_name="foo")
        skel.write(self.tmp_dir.path)

        foo_path = os.path.join(self.tmp_dir.path, 'foo.txt')
        with open(foo_path) as foo_file:
            self.assertEqual(foo_file.read().strip(), 'foo')


def suite():
    """Return all tests for skeleton.Skeleton"""
    return unittest.TestLoader().loadTestsFromTestCase(TestSkeleton)

if __name__ == "__main__":
    unittest.main()
