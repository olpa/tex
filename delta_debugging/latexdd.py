import os, sys, re
import DD
import runlatex, decider

delta_mode = 'lines'

#
# LaTeX file consist of parts:
# * classname       - {} part of \documentclass
# * classoptions    - [] part of \documentclass
# * preamble        - everything after \documentclass{} till \begin{document}
# * document        - inside \begin{document}...\end{document}
# Parsing is fragile.
#
re_dclass = re.compile('\\\\documentclass(\\[([^]]*)\\])?\{([^}]*)\}\\s*')
class LatexFile:
  def __init__(self, fname):
    self.deltas = None
    if fname is None:
      return
    self.file_name = fname
    h = open(fname)
    s = h.read()
    h.close()
    m = re_dclass.search(s)
    if not m:
      raise Exception("\\documentclass not found")
    self.classoptions = m.group(2)
    self.classname    = m.group(3)
    s = s[m.end():]
    pos = s.index('\\begin{document}')
    self.preamble = s[:pos].strip()
    pos2 = s.index('\\end{document}')
    self.document = s[16+pos:pos2].strip()

  #
  # Save file
  #
  def write_stream(self, h):
    h.write('\\documentclass')
    if self.classoptions:
      h.write('[%s]' % self.classoptions)
    h.write("{%s}" % self.classname)
    if self.preamble:
      h.write("\n")
      h.write(self.preamble)
    h.write("\n\\begin{document}\n")
    h.write(self.document)
    h.write("\n\\end{document}\n")

  def write_file(self, fname):
    h = open(fname, 'w')
    self.file_name = fname
    self.write_stream(h)
    h.close()

  #
  # Each delta is one character. Not effective, but straightforward.
  # Technically, a delta is a three-item entry: (where, index, letter):
  # * where  - O (options), N (name), P (preamble), D (document)
  # * index&letter - which letter to change
  #
  def create_deltas(self):
    deltas = []
    if 'minimal' != self.classname:
      deltas.append(('N', None, None))
    def process_part(where, s):
      index = 1
      if s is not None:
        if 'lines' == delta_mode:
          s = s.split("\n")
          s = [l+"\n" for l in s]
          print >>sys.stderr, "!!!!! Lines mode"
        for ch in s:
          deltas.append((where, index, ch))
          index = index + 1
    process_part('O', self.classoptions)
    process_part('P', self.preamble)
    process_part('D', self.document)
    self.deltas = deltas
    return deltas

  def get_deltas(self):
    if self.deltas is None:
      self.create_deltas()
    return self.deltas
  
  #
  # Apply deltas
  # According to DD documentation, the deltas are sorted
  #
  def apply_deltas(self, deltas):
    lf = LatexFile(None)
    lf.file_name = self.file_name
    lf.classname = 'minimal'
    lf.classoptions = lf.preamble = lf.document = ''
    for (where, index, ch) in deltas:
      if 'D' == where:
        lf.document = lf.document + ch
      elif 'P' == where:
        lf.preamble = lf.preamble + ch
      elif 'O' == where:
        lf.classoptions = lf.classoptions + ch
      elif 'N' == where:
        lf.classname = self.classname
      else:
        raise Exception("Unsupported delta: " + where)
    return lf

  #
  # Execute
  #
  def run_latex(self):
    rundir = runlatex.create_run_dir()
    fname = os.path.basename(self.file_name)
    self.write_file(os.path.join(rundir, fname))
    self.errors = runlatex.run_latex_collect_errors(rundir, fname)

  def get_errors(self):
    return self.errors

#
# DD
#
class LatexDD(DD.DD):
  def __init__(self, fname, ok_is=decider.PASS_NO_ERRORS, fail_is=decider.FAIL_MASTER_ERRORS):
    DD.DD.__init__(self)
    self.lf = LatexFile(fname)
    self.last_run = None
    self.decider = decider.decider(ok_is, fail_is)
    self.decider.extract_master_errors(self.lf)
    self.decider.sanity_check(self)

  def _test(self, deltas):
    lf = self.lf.apply_deltas(deltas)
    lf.run_latex()
    self.last_run = lf
    return self.decider.get_result(lf)

  def get_last_run(self):
    return self.last_run

  def test_with_no_deltas(self):
    return self._test([])

  def test_with_all_deltas(self):
    return self._test(self.get_deltas())

  def create_deltas(self):
    return self.lf.create_deltas()

  def show_applied_delta(self, deltas, h):
    lf = self.lf.apply_deltas(deltas)
    lf.write_stream(h)

  def coerce(self, c):
    if len(c) < 10:
      s = str(c)
    else:
      s = str(c[:10]) + '........'
    return s

  def get_deltas(self):
    return self.lf.get_deltas()

  def get_master_errors(self):
    return self.decider.get_master_errors()

# ---------------------------------------------------------

def main():
  fname = sys.argv[1]
  runlatex.guess_latex_tool(fname)
  dd = LatexDD(fname)
  print 'Master errors:'
  print dd.get_master_errors()
  if '--stop-after-master' in sys.argv:
    sys.exit()
  deltas = dd.create_deltas()
  c = dd.ddmin(deltas)
  print 'The 1-minimal failure-inducing input is:'
  print '----------------------------------------'
  dd.show_applied_delta(c, sys.stdout)

if '__main__' == __name__:
  main()
