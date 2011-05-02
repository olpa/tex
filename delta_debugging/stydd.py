import os, sys
import DD
import runlatex

class OneCharDeltaFile:
  def __init__(self, fname, mode):
    h = open(fname)
    if 'char' == mode:
      self.content = h.read()
    elif 'line' == mode:
      self.content = h.readlines()
    else:
      raise Exception("Unknown mode:" + mode)
    h.close()

  def get_deltas(self):
    return list(range(len(self.content)))

  def apply_deltas(self, deltas):
    s = ''
    for i in deltas:
      s = s + self.content[i]
    return s

  def write_stream(self, h, deltas):
    h.write(self.apply_deltas(deltas))

  def write_file(self, fname, deltas):
    h = open(fname, 'w')
    self.write_stream(h, deltas)
    h.close()

class StyDD(DD.DD):
  def __init__(self, tex_file, sty_file, mode):
    DD.DD.__init__(self)
    self.tex_file = os.path.basename(tex_file)
    self.sty_file = os.path.basename(sty_file)
    self.ocdf = OneCharDeltaFile(sty_file, mode)
    self.master_errors = self.run_latex_return_errors(self.ocdf.get_deltas())

  def run_latex_return_errors(self, deltas):
    rundir = runlatex.create_run_dir()
    self.ocdf.write_file(os.path.join(rundir, self.sty_file), deltas)
    return runlatex.run_latex_collect_errors(rundir, self.tex_file)

  def _test(self, deltas):
    errors = self.run_latex_return_errors(deltas)
    if '' == errors:
      return self.PASS
    if self.master_errors == errors:
      return self.FAIL
    return self.UNRESOLVED

  def coerce(self, c):
    if len(c) < 10:
      s = str(c)
    else:
      s = str(c[:10]) + '........'
    return s

  def show_applied_delta(self, h, deltas):
    self.ocdf.write_stream(h, deltas)

  def get_deltas(self):
    return self.ocdf.get_deltas()

if '__main__' == __name__:
  mode     = 'char'
  out_file = None
  argv     = sys.argv[1:]
  if '-o' in argv:
    i = argv.index('-o')
    out_file = argv[i+1]
    del argv[i:i+2]
  if '--lines' in argv:
    mode = 'line'
    argv.remove('--lines')
  (tex_file, sty_file) = argv
  runlatex.guess_latex_tool(tex_file)
  dd = StyDD(tex_file, sty_file, mode)
  print 'Master errors:'
  print dd.master_errors
  if '' == dd.master_errors:
    print 'No errors, exiting'
    sys.exit(-1)
  deltas = dd.get_deltas()
  c = dd.ddmin(deltas)
  print 'The 1-minimal failure-inducing sty input is:'
  print '--------------------------------------------'
  if out_file is None:
    h = sys.stdout
  else:
    h = open(out_file, 'w')
    print "In the file", out_file
  dd.show_applied_delta(h, c)
  if out_file is not None:
    h.close()
