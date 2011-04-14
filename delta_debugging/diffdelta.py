import os, sys, difflib
import DD
import runlatex

class DiffDelta:

  def __init__(self, fname_pass, fname_fail):
    self.lines_pass = open(fname_pass, 'U').readlines()
    self.lines_fail = open(fname_fail, 'U').readlines()
    diff = difflib.SequenceMatcher(None, self.lines_pass, self.lines_fail)
    self.opcodes = diff.get_opcodes()

  def get_deltas(self):
    deltas = []
    i = 0
    for tag, _, _, _, _ in self.opcodes:
      if 'equal' != tag:
        deltas.append(i)
      i = i + 1
    return deltas

  def write_stream(self, h, deltas):
    i = -1
    for (tag, a1, a2, b1, b2) in self.opcodes:
      i = i + 1
      if i not in deltas:
        tag = 'equal'
      if ('replace' == tag) or ('insert' == tag):
        ll = self.lines_fail[b1:b2]
      elif 'delete' == tag:
        continue
      elif 'equal' == tag:
        ll = self.lines_pass[a1:a2]
      else:
        raise Exception("Unknown tag: " + tag)
      for l in ll:
        h.write(l)

  def write_file(self, fname, deltas):
    h = open(fname, 'w')
    self.write_stream(h, deltas)
    h.close()

  def write_diff(self, h, deltas):
    def write_range(x1, x2):
      if x1 == x2:
        h.write(str(x1))
      else:
        h.write("%i,%i" % (x1+1, x2))
    def write_tag(tag):
      if 'replace' == tag:
        h.write('c')
      elif 'delete' == tag:
        h.write('d')
      elif 'insert' == tag:
        h.write('a')
      else:
        raise Exception("Unknown diff tag: " + tag)
    for i in deltas:
      (tag, a1, a2, b1, b2) = self.opcodes[i]
      write_range(a1, a2)
      write_tag(tag)
      write_range(b1, b2)
      h.write("\n")
      for l in self.lines_pass[a1:a2]:
        h.write("< " + l)
      if (a1 != a2) and (b1 != b2):
        h.write("---\n")
      for l in self.lines_fail[b1:b2]:
        h.write("> " + l)

class DiffDeltaDD(DD.DD):
  def __init__(self, tex_file, sty_pass, sty_fail):
    DD.DD.__init__(self)
    self.diff = DiffDelta(sty_pass, sty_fail)
    self.tex_file = os.path.basename(tex_file)
    self.sty_name = os.path.basename(sty_pass)
    if self.sty_name != os.path.basename(sty_fail):
      print "The names of sty-files should match"
      sys.exit(-1)
    no_errors = self.run_latex(())
    if '' != no_errors:
      print "Compiling against the 'pass' sty should produce no errors, but:"
      print no_errors
      sys.exit(-1)
    self.master_errors = self.run_latex(self.diff.get_deltas())
    print "Master errors:"
    print self.master_errors
    if '' == self.master_errors:
      print "Compiling against 'fail' sty should produce errors"
      sys.exit(-1)

  def run_latex(self, deltas):
    rundir = runlatex.create_run_dir()
    self.diff.write_file(os.path.join(rundir, self.sty_name), deltas)
    return runlatex.run_latex_collect_errors(rundir, self.tex_file)

  def _test(self, deltas):
    errors = self.run_latex(deltas)
    if '' == errors:
      return self.PASS
    if self.master_errors == errors:
      return self.FAIL
    return self.UNRESOLVED

  def get_deltas(self):
    return self.diff.get_deltas()

if '__main__' == __name__:
  (tex_file, fname_pass, fname_fail) = sys.argv[1:]
  runlatex.guess_latex_tool(tex_file)
  dd = DiffDeltaDD(tex_file, fname_pass, fname_fail)
  deltas = dd.get_deltas()
  c = dd.ddmin(deltas)
  print 'The 1-minimal failure-inducing delta is:'
  print '----------------------------------------'
  dd.diff.write_diff(sys.stdout, c)
