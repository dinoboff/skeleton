import unittest

import testskeleton
import testvar
import testdefaulttemplate

try:
    import testbasicpackage
except Exception:
    TestBasicPackage = None


def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(testskeleton.suite())
    suite.addTest(testvar.suite())
    
    if hasattr('', 'format'):
        suite.addTest(testbasicpackage.suite())
        suite.addTest(testdefaulttemplate.suite())
    
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())