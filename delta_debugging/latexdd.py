tmpdir          = 'tmp'
rundir_basename = 'run'
latex_cmdline   = 'latex -interaction batchmode -output-directory ${RUNDIR} ${FILENAME} 2>&1 >${RUNDIR}/stdout.txt'

import os, tempfile, string, sys, re

#
# Create a directory to run TeX. Design decision name:
#      ./tmp/run
# If exist, first rename existing, then create new.
#
def create_run_dir(tmpdir, rundir_basename):
  rundir = os.path.join(tmpdir, rundir_basename)
  if os.path.isdir(rundir):
    tempfile.tempdir = tmpdir
    newdir = tempfile.mktemp(prefix='run_')
    os.rename(rundir, newdir)
  os.makedirs(rundir)
  return rundir

def run_latex(rundir, filename):
  sub = {
      'RUNDIR':   rundir,
      'FILENAME': filename
      }
  cmdline = string.Template(latex_cmdline).substitute(sub)
  os.system(cmdline)

#
# errors: everything what starts with '! ' in log
#
def collect_errors(rundir, tex_file):
  logfile = os.path.join(rundir, os.path.splitext(os.path.basename(tex_file))[0] + '.log')
  s_errors = ''
  h = open(logfile)
  for l in h:
    if '! ' == l[:2]:
      s_errors = s_errors + l
  h.close()
  return s_errors

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
    h = open(fname)
    s = h.read()
    h.close()
    m = re_dclass.search(s)
    if not m:
      raise Exception("\\documentclass not found")
    self.classoptions = m.group(2)
    s = s[m.end():]
    pos = s.index('\\begin{document}')
    self.preamble = s[:pos].strip()
    pos2 = s.index('\\end{document}')
    self.document = s[16+pos:pos2].strip()

if '__main__' == __name__:
  fname = sys.argv[1]
  #rundir = create_run_dir(tmpdir, rundir_basename)
  #run_latex(rundir, fname)
  #print collect_errors(rundir, fname)
  lf = LatexFile(fname)
