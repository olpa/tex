tmpdir          = 'tmp'
rundir_basename = 'run'
latex_tool      = 'latex'
latex_cmdline   = '(ulimit -t 30; echo -n '' | ${LATEX} -interaction batchmode -output-directory ${RUNDIR} ${FILENAME}) 2>&1 >${RUNDIR}/stdout.txt'
latex_max_rerun = 3

import os, tempfile, string, re

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
  h = open(logfile)
  b_extract_command = 0
  for l in h:
    if b_extract_command:
      pos = l.rfind(' ',0, -2) # ignore trailing ' '
      s_errors = s_errors + l[1+pos:]
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
    if 'LaTeX Warning: ' in l:
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
