import os, sys, re
import DD
import runlatex, decider

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
    s = s + "\n\n\\RequirePackage{ddstub}\n"
    return s

  def write_stream(self, h, deltas):
    h.write(self.apply_deltas(deltas))

  def write_file(self, fname, deltas):
    h = open(fname, 'w')
    self.write_stream(h, deltas)
    h.close()

class StyDD(DD.DD):
  def __init__(self, tex_file, sty_file, mode, digger=None):
    DD.DD.__init__(self)
    self.digger = digger
    self.tex_file = tex_file
    self.sty_file = os.path.basename(sty_file)
    self.last_run = None
    self.ocdf = OneCharDeltaFile(sty_file, mode)
    self.s_stub = generate_stub_from_sty(sty_file)
    self.decider = decider.decider()
    self.decider.extract_master_errors(self)

  def run_latex_return_errors(self, deltas):
    self.last_run = runlatex.RunLatex(digger=self.digger, hook_before_run=self.hook_before_run)
    rundir = self.last_run.create_run_dir()
    self.ocdf.write_file(os.path.join(rundir, self.sty_file), deltas)
    return self.last_run.run_latex_collect_errors(self.tex_file)

  def hook_before_run(self, run_latex):
    dname = self.last_run.get_run_dir()
    fname = os.path.join(dname, 'ddstub.sty')
    h = file(fname, 'w')
    h.write(self.s_stub)
    h.close()

  def get_last_run(self):
    return self.last_run

  def _test(self, deltas):
    errors = self.run_latex_return_errors(deltas)
    return self.decider.get_result(self.last_run)

  def test_with_no_deltas(self):
    self.run_latex_return_errors([])

  def test_with_all_deltas(self):
    self.run_latex_return_errors(self.get_deltas())

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

re_def = re.compile(r'''(\\newcommand|\\newenvironment)\{?(\\?[^\{\}\[\]]+)\}?(\[\d+\])?''')

def generate_stub_from_sty(fname):
  h = open(fname)
  s = h.read()
  h.close()
  s_sty = "\\ProvidesPackage{ddstub}[]\n\n"
  for m in re_def.findall(s):
    (what, cmd_name, args) = m
    if 'command' in what:
      s_sty = s_sty + ("\\providecommand%s%s{}\n" % (cmd_name, args))
    else:
      s_sty = s_sty + ("\\provideenvironment{%s}%s{}{}\n" % (cmd_name, args))
  return s_sty

def main(digger=None):
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
  stop_after_master = '--stop-after-master' in argv
  if stop_after_master:
    argv.remove('--stop-after-master')
  (tex_file, sty_file) = argv
  runlatex.guess_latex_tool(tex_file)
  dd = StyDD(tex_file, sty_file, mode, digger=digger)
  dd.decider.print_master_errors()
  if stop_after_master:
    sys.exit()
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

if '__main__' == __name__:
  main()
