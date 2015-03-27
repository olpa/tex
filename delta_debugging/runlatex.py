class RunEnv:
  def __init__(self):
    self.tool = 'pdflatex'
    self.cmdline = '(ulimit -t 30; echo -n '' | ${LATEX} -interaction batchmode -output-directory ${RUNDIR} ${EXTRAOPT} ${FILENAME}) 2>&1 >${RUNDIR}/stdout.txt'
    self.extra_latex_opt = ''
    self.texinputs = None
    self.tmpdir = 'tmp'
    self.rundir = 'run'
    self.max_reruns = 3
    self.rundir_created = 0
  def set_rundir(self, rundir):
    self.rundir = rundir
  def get_rundir(self):
    return self.rundir
  def set_latex_tool(self, tool):
    self.tool = tool
  def set_extra_latex_opt(self, opt):
    self.extra_latex_opt = opt
  def set_texinputs(self, ti):
    self.texinputs = ti

import sys, os, tempfile, string, re, shutil

#
# Create a directory to run TeX. Design decision name:
#      ./tmp/run
# If exist, first rename existing, then create new.
#
def create_run_dir(env):
  if env.rundir_created:
    return self.rundir
  rundir = os.path.join(env.tmpdir, env.rundir)
  if os.path.isdir(rundir):
    tempfile.tempdir = env.tmpdir
    newdir = tempfile.mktemp(prefix=env.rundir+'_')
    os.rename(rundir, newdir)
  os.makedirs(rundir)
  env.set_rundir(rundir)
  env.rundir_created = 1
  return rundir

def run_latex(env, filename):
  sub = {
      'RUNDIR':   env.rundir,
      'FILENAME': filename,
      'LATEX':    env.tool,
      'EXTRAOPT': env.extra_latex_opt,
      }
  cmdline = string.Template(env.cmdline).substitute(sub)
  orig_ti = os.environ.get('TEXINPUTS', None)
  revert_ti = 0
  if env.texinputs:
    ti = orig_ti or ''
    ti = '.' + os.pathsep + env.texinputs + os.pathsep + ti
    os.environ['TEXINPUTS'] = ti
    revert_ti = 1
  #print "!!!! going to run:", cmdline, 'TEXINPUTS:', os.environ.get('TEXINPUTS', None)
  #s = sys.stdin.readline()
  ccode = os.system(cmdline)
  if revert_ti:
    if orig_ti is None:
      del os.environ['TEXINPUTS']
    else:
      os.environ['TEXINPUTS'] = orig_ti
  return ccode

#
# errors: everything what starts with '! ' in log
# Improvement: return only the first error.
#
re_page = re.compile('page\\s+\\d+')
re_line = re.compile('line\\s+\\d+')
def collect_errors(env, tex_file):
  logfile = os.path.join(env.get_rundir(), os.path.splitext(os.path.basename(tex_file))[0] + '.log')
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

def run_latex_collect_errors(env, fname):
  i = 0
  while 1:
    ccode = run_latex(env, fname)
    if ccode > 256:
      return "! HANG\n"                                    # return
    s = collect_errors(env, fname)
    i = i + 1
    if ('Rerun to get' in s) and (i < env.max_reruns):
      continue
    return s                                               # return

#
# Read a few first lines and find:
# % !TEX TS-program = latex_tool
#
def guess_latex_tool(env, fname):
  h = open(fname)
  s = h.read(1024)
  h.close()
  m = re.search('%\\s*!TEX\\s+TS-program\\s*=\\s*(\w+)', s)
  if m:
    latex_tool = m.group(1).lower()
    env.set_latex_tool(latex_tool)

#
# Object-wrapper for functions above
#
class RunLatex:

  def __init__(self, env, digger=None, hook_before_run=None):
    self.env = env
    self.digger = digger
    self.hook_before_run = hook_before_run
    self.errors = ''
    self.reference = ''
    self.tex_file = None

  def create_run_dir(self):
    create_run_dir(self.env)
    return self.env.get_rundir()

  def get_run_dir(self):
    return self.env.get_rundir()

  def run_latex_collect_errors(self, tex_file):
    d1 = os.path.normpath(os.path.abspath(self.env.get_rundir()))
    d2 = os.path.normpath(os.path.abspath(os.path.dirname(tex_file)))
    if d1 != d2:
      fname2 = os.path.join(d1, os.path.basename(tex_file))
      shutil.copy(tex_file, fname2)
      tex_file = fname2
    self.tex_file = tex_file
    if self.hook_before_run:
      self.hook_before_run(self)
    self.errors = run_latex_collect_errors(self.env, tex_file)
    if self.digger:
      self.reference = self.digger(self)

  def get_errors(self):
    return self.errors

  def get_reference(self):
    return self.reference

  def get_log_file_name(self):
    return os.path.splitext(self.tex_file)[0] + '.log'
