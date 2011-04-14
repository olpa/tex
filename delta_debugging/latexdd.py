import os, sys, re
import DD
import runlatex

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
        for ch in s:
          deltas.append((where, index, ch))
          index = index + 1
    process_part('O', self.classoptions)
    process_part('P', self.preamble)
    process_part('D', self.document)
    return deltas
  
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
  def run_latex_return_errors(self):
    rundir = runlatex.create_run_dir()
    fname = os.path.basename(self.file_name)
    self.write_file(os.path.join(rundir, fname))
    return runlatex.run_latex_collect_errors(rundir, fname)

#
# DD
#
class LatexDD(DD.DD):
  def __init__(self, fname):
    DD.DD.__init__(self)
    self.lf = LatexFile(fname)
    self.master_errors = self.lf.run_latex_return_errors()

  def _test(self, deltas):
    lf = self.lf.apply_deltas(deltas)
    errors = lf.run_latex_return_errors()
    if '' == errors:
      return self.PASS
    if self.master_errors == errors:
      return self.FAIL
    return self.UNRESOLVED

  def create_deltas(self):
    return self.lf.create_deltas()

  def show_applied_delta(self, deltas, h):
    lf = self.lf.apply_deltas(deltas)
    lf.write_stream(h)

# ---------------------------------------------------------

if '__main__' == __name__:
  fname = sys.argv[1]
  dd = LatexDD(fname)
  deltas = dd.create_deltas()
  c = dd.ddmin(deltas)
  print 'The 1-minimal failure-inducing input is:'
  print '----------------------------------------'
  dd.show_applied_delta(c, sys.stdout)
