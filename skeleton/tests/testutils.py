"""
Test in skeleton.utils.*
"""
from __future__ import with_statement

import os
import unittest

from skeleton.tests.utils import TestCase
from skeleton.utils import insert_into_file


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

def suite():
    """Return tests for skeleton.utils.*  """
    return unittest.TestLoader().loadTestsFromTestCase(TestInsertIntoFile)


if __name__ == "__main__":
    unittest.main()
