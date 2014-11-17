import glob, os, new, sys
import unittest
import LatexTest

#
# Settings
#
class Settings:
  def __init__(self):
    sty_dir = os.path.normpath(os.path.join(os.getcwd(), '..', 'dev'))
    old_ti = os.getenv('TEXINPUTS', '')
    os.environ['TEXINPUTS'] = sty_dir + ':' + old_ti
  def get_tmp_dir(self):
    return 'tmp'
  def get_latex(self):
    return 'pdflatex'
LatexTest.settings = Settings()

#
# Collect tests
#
filter = None
if len(sys.argv) > 1:
  filter = sys.argv[1]
test_files = glob.glob('*/test_*.tex')
test_files = [x for x in test_files if 'visual_tables' not in x]
modules_and_tests = {}
for fname in test_files:
  (dir, basename) = os.path.split(fname)
  if 'tmp' == dir:
    continue
  if filter:
    if filter not in fname:
      continue
  modules_and_tests.setdefault(dir, []).append(basename)

#
# Test function
#
def generic_test_func(self, modname, testname):
  print 'I am a test case with parameters:', self.__class__, modname, testname
  self.assertEqual(1, 1)

#
# Create test classes and functions
#
test_classes = []
for module in modules_and_tests.iterkeys():
  mtname = 'Test' + module.capitalize()
  cls = new.classobj(mtname, (LatexTest.LatexTestCase,), {})
  for test_file in modules_and_tests[module]:
    test_name = os.path.splitext(test_file)[0]
    def get_test_func(func, module, test_name):
      def proxied(self):
        func(self, module, test_name)
      return proxied
    setattr(cls, test_name, get_test_func(LatexTest.LatexTestCase.run_test_case, module, test_name))
  test_classes.append(cls)

#
# Run the tests
#
if __name__ == '__main__':
  tl = unittest.TestLoader()
  tests = [tl.loadTestsFromTestCase(x) for x in test_classes]
  tests = unittest.TestSuite(tests)
  unittest.TextTestRunner(verbosity=2).run(tests)
