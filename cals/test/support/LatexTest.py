# Running a latex
import unittest, os, shutil, re, glob

settings = None # will be set from the main script

re_macro_start = re.compile(r'''^> \\[^=]+=macro:$''')
re_box_start = re.compile(r'''^> \\box\d+=''')
re_some_show = re.compile(r'''^> .*\.$''')
re_message   = re.compile(r'''^! ''')
re_comment   = re.compile(r'''^%[^\r\n]*[\r\n]*''', re.S|re.M)

class LatexTestCase(unittest.TestCase):

  def __init__(self, *ls):
    unittest.TestCase.__init__(self, *ls)
    tpl_file = 'template.txt'
    h = open(tpl_file)
    self.template = h.read()
    h.close()

  def get_settings(self):
    return settings

  def setUp(self):
    tmp_dir = settings.get_tmp_dir()
    for fname in os.listdir(tmp_dir):
      full_name = os.path.join(tmp_dir, fname)
      os.unlink(full_name)

  def run_latex(self, module, test_name):
    tmp_dir = settings.get_tmp_dir()
    src_latex_file = os.path.join(module, test_name + '.tex')
    tmp_latex_file = os.path.join(tmp_dir, test_name + '.tex')
    tmp_log_file   = os.path.join(tmp_dir, test_name + '.log')
    #
    # Create a TeX file from a tempate
    #
    h = open(src_latex_file)
    s = h.read()
    h.close()
    s = self.template.replace('##CODE##', s)
    h = open(tmp_latex_file, 'w')
    h.write(s)
    h.close()
    #
    # Run LaTeX
    #
    cmd = 'cd %s; %s -interaction batchmode %s.tex >/dev/null' % (tmp_dir, settings.get_latex(), test_name)
    os.system(cmd)
    return tmp_log_file

  # -------------------------------------------------------
  # Log-file works

  #
  # Comparing expected and the got results
  #
  def check_log(self, module, test_name, log_file):
    s_got = self.collect_log(log_file)
    chk_file = os.path.join(module, test_name + '.chk')
    h = open(chk_file)
    s_expected = h.read()
    h.close()
    s_expected = re_comment.sub('', s_expected)
    s_expected = s_expected.strip()
    s_got      = s_got.strip()
    #
    # It is convenient to know where exactly start difference
    #
    if s_expected != s_got:
      pos = 0
      maxpos = min(len(s_expected), len(s_got))
      while (pos < maxpos) and (s_expected[pos] == s_got[pos]):
        pos = pos +1
      s_expected = s_expected[:pos] + '---->' + s_expected[pos:]
      s_got      = s_got[:pos]      + '---->' + s_got[pos:]
    self.assertEqual(s_got, s_expected)

  #
  # The test case: run latex and check log
  #
  def run_test_case(self, module, test_name):
    log_file = self.run_latex(module, test_name)
    self.check_log(module, test_name, log_file)
    self.check_pdf(module, test_name)

  #
  # Log parsing
  #
  def collect_macro(self, h, macro_dump):
    for l in h:
      l = l.strip()
      macro_dump = macro_dump + "\n" + l
      if (len(l) > 0) and ('.' == l[-1]):
        break
    return macro_dump

  def collect_box(self, h, box_dump):
    box_dump = re.sub('[0-9]+', 'XX', box_dump)
    for l in h:
      l = l.strip()
      if '' == l:
        break
      box_dump = box_dump + "\n" + l
    return box_dump

  def collect_log(self, log_file):
    s = ''
    h = open(log_file)
    for l in h:
      l = l.strip()
      if re_macro_start.match(l):
        macro_dump = self.collect_macro(h, l)
        s = s + macro_dump + "\n"
      if re_box_start.match(l):
        box_dump = self.collect_box(h, l)
        s = s + box_dump + "\n"
      if re_some_show.match(l):
        s = s + l + "\n"
      if re_message.match(l):
        if l != '! OK.':
          s = s + l + "\n"
      if l.startswith('Package test Info: '):
        pos = l.index('on input line ')
        s = s + l[19:pos]
        s = s.rstrip()
        s = s + "\n"
    return s

  # -------------------------------------------------------
  # Output works

  def check_pdf(self, module, test_name):
    #
    # First, check if output testing is required
    #
    expected_pngs = glob.glob(os.path.join(module, test_name+'*.png'))
    if not len(expected_pngs):
      return
    expected_pngs = [os.path.basename(x) for x in expected_pngs]
    #
    # Generate PNGs and check we got the same number of files
    #
    tmp_dir = settings.get_tmp_dir()
    cmd = "cd %s; convert -density 300x300 %s.pdf %s.png" % (tmp_dir, test_name, test_name)
    os.system(cmd)
    got_pngs = glob.glob(os.path.join(tmp_dir, test_name+'*.png'))
    got_pngs = [os.path.basename(x) for x in got_pngs]
    self.assertEqual(expected_pngs, got_pngs)
    #
    # Compare the PNGs
    #
    for png in expected_pngs:
      expected_png = os.path.join(module, png)
      got_png      = os.path.join(tmp_dir, png)
      diff_png     = os.path.join(tmp_dir, 'diff.png')
      cmd = "compare compare -metric RMSE %s %s %s 2>%s" % (expected_png, got_png, diff_png, os.path.join(tmp_dir, 'compare-stdout'))
      os.system(cmd)
      h = open(os.path.join(tmp_dir, 'compare-stdout'))
      s = h.read()
      h.close()
      s = s.strip()
      self.assertEqual('0 (0)', s)
