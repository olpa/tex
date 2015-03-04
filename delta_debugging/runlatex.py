tmpdir          = 'tmp'
rundir_basename = 'run'
latex_tool      = 'latex'
latex_cmdline   = '(ulimit -t 30; echo -n '' | ${LATEX} -interaction batchmode -output-directory ${RUNDIR} ${FILENAME}) 2>&1 >${RUNDIR}/stdout.txt'
latex_max_rerun = 3

import sys, os, tempfile, string, re, shutil

if os.path.isdir('texinput'):
  dirname = os.path.abspath('texinput')
  os.environ['TEXINPUTS'] = dirname + ':' + os.environ.get('TEXINPUTS', '')

#
# Create a directory to run TeX. Design decision name:
#      ./tmp/run
# If exist, first rename existing, then create new.
#
def create_run_dir(tmpdir=tmpdir, rundir_basename=rundir_basename):
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
      'FILENAME': filename,
      'LATEX':    latex_tool
      }
  cmdline = string.Template(latex_cmdline).substitute(sub)
  #print "!!!! going to run:", cmdline # FIXME
  #s = sys.stdin.readline() # FIXME
  return os.system(cmdline)

#
# errors: everything what starts with '! ' in log
# Improvement: return only the first error.
#
re_page = re.compile('page\\s+\\d+')
re_line = re.compile('line\\s+\\d+')
def collect_errors(rundir, tex_file):
  logfile = os.path.join(rundir, os.path.splitext(os.path.basename(tex_file))[0] + '.log')
  s_errors = ''
  try:
    h = open(logfile)
  except IOError:
    return "! LOG FILE MISSED\n"
  b_extract_command = 0
  for l in h:
    if b_extract_command:
      pos = l.rfind(' ',0, -2) # ignore trailing ' '
      s_errors = s_errors + l[1+pos:]
      b_extract_command = 0
      continue
    if 'LaTeX warning' in l:
      continue
    if '! ' == l[:2]:
      s_errors = s_errors + l
      if '! Undefined control sequence' in l:
        s_errors = s_errors.rstrip() + ' '
        b_extract_command = 1
      continue
    if '### ' == l[:4]: # ### begingroup/endgroup wrong nesting 
      s_errors = s_errors + l[:15] + "\n"
      continue
    if 'Rerun to get' in l:
      s_errors = s_errors + l
      continue
  h.close()
  s_errors = re_page.sub('page NNN', s_errors)
  s_errors = re_line.sub('line NNN', s_errors)
  return s_errors

def run_latex_collect_errors(rundir, fname):
  i = 0
  while 1:
    ccode = run_latex(rundir, fname)
    if ccode > 256:
      return "! HANG\n"                                    # return
    s = collect_errors(rundir, fname)
    i = i + 1
    if ('Rerun to get' in s) and (i < latex_max_rerun):
      continue
    return s                                               # return

#
# Read a few first lines and find:
# % !TEX TS-program = latex_tool
#
def guess_latex_tool(fname):
  global latex_tool
  h = open(fname)
  s = h.read(1024)
  h.close()
  m = re.search('%\\s*!TEX\\s+TS-program\\s*=\\s*(\w+)', s)
  if m:
    latex_tool = m.group(1).lower()

#
# Object-wrapper for functions above
#
class RunLatex:

  def __init__(self, digger=None):
    self.digger = digger
    self.rundir = None
    self.errors = ''
    self.reference = ''
    self.tex_file = None

  def create_run_dir(self):
    self.rundir = create_run_dir()
    return self.rundir

  def run_latex_collect_errors(self, tex_file):
    d1 = os.path.normpath(os.path.abspath(self.rundir))
    d2 = os.path.normpath(os.path.abspath(os.path.dirname(tex_file)))
    if d1 != d2:
      fname2 = os.path.join(d1, os.path.basename(tex_file))
      shutil.copy(tex_file, fname2)
      tex_file = fname2
    self.tex_file = tex_file
    self.errors = run_latex_collect_errors(self.rundir, tex_file)
    if self.digger:
      self.reference = self.digger(self)

  def get_errors(self):
    return self.errors

  def get_reference(self):
    return self.reference

  def get_log_file_name(self):
    return os.path.splitext(self.tex_file)[0] + '.log'
